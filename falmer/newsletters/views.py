import datetime

import requests
from django.conf import settings
from django.http import Http404, HttpResponse
from mailchimp3 import MailChimp
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.crypto import get_random_string

from .models import MailChimpList, NewsletterResumeToken


def get_mailchimp_client():
    client = MailChimp(
        settings.MAILCHIMP_API_KEY,
        settings.MAILCHIMP_API_USERNAME,
        timeout=10.0
    )

    return client


class MailchimpError(Exception):
    pass


def get_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


class ListMembersAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, list_slug):
        try:
            list = MailChimpList.objects.get(slug=list_slug, enabled=True)
        except MailChimpList.DoesNotExist:
            raise Http404

        client = get_mailchimp_client()

        try:
            mc_response = client.lists.members.create(list_id=list.mailchimp_list_id, data={
                'status': 'pending',
                'email_address': request.data['email_address'],
                'ip_signup': get_ip(request)
            })
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                json = e.response.json()

                if json.get('title') == 'Member Exists':
                    # this is definitely the correct usage of this
                    return Response({'complete': True, }, status=status.HTTP_200_OK)

                raise MailchimpError(json.get('errors') or json.get('detail') or json)
            else:
                return HttpResponse(status=500)

        continuation_token = get_random_string(16)
        NewsletterResumeToken.objects.create(
            list=list,
            email_id=mc_response['id'],
            continuation_token=continuation_token,
        )

        return Response({'continuationToken': continuation_token, }, status=status.HTTP_200_OK)

    def patch(self, request, list_slug):
        try:
            mc_list = MailChimpList.objects.get(slug=list_slug, enabled=True)
        except MailChimpList.DoesNotExist:
            raise Http404

        try:
            resume_token = NewsletterResumeToken.objects.get(
                continuation_token=request.data['continuationToken'],
                list=mc_list
            )
        except NewsletterResumeToken.DoesNotExist:
            raise Http404

        if resume_token.created_at < timezone.now() - datetime.timedelta(hours=48):
            return Response({
                'error': 'continuation token expired',
            }, status=status.HTTP_401_UNAUTHORIZED)

        client = get_mailchimp_client()

        try:
            mc_response = client.lists.members.update(
                list_id=mc_list.mailchimp_list_id,
                subscriber_hash=resume_token.email_id,
                data={
                'merge_fields': request.data['fields'],
            })
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                json = e.response.json()
                return Response({'error': json.get('errors') or json.get('detail')}, status=500)
            else:
                return HttpResponse(status=500)

        return Response(status=status.HTTP_200_OK)
