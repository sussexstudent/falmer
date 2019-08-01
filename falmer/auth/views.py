import jwt
from django import forms
from django.conf import settings
from django.contrib.auth import login, logout
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

from falmer.auth.serializers import MeSerializer
from falmer.auth.utils import create_magic_link_for_user
from .models import MagicLinkToken, FalmerUser


def magic_link_login(request, token):
    try:
        magic = MagicLinkToken.objects.get(token=token, used=False)
    except MagicLinkToken.DoesNotExist:
        return JsonResponse({'error': 'Token not found'})

    magic.used = True
    magic.save()
    login(request, magic.user)

    return redirect('/')


def sso(request):

    # get qs token=?

    try:
        token = request.GET.get('token')

        claim = jwt.decode(token, settings.BOWTIE_SECRET, algorithms='HS256')

        is_used = cache.get(f'sso:{claim["jwtid"]}', False)

        if is_used:
            raise PermissionError()

        cache.set(f'sso:{claim["jwtid"]}', True, 60)

        try:
            user = FalmerUser.objects.get(identifier__iexact=claim['id'])
        except FalmerUser.DoesNotExist:
            user = FalmerUser.objects.create(
                identifier=claim['id'],
                authority='IS',
            )

        user.ensure_ambient_permissions()

        login(request, user)

        return redirect('/')

    except KeyError:
        raise PermissionError()


class RequestLoginForm(forms.Form):
    email = forms.EmailField(label='Your @sussexstudent.com address', max_length=100)


def email_link_sent(request):
    return render(request, 'auth/link_sent.html')


def email_link_request(request):
    if request.method == 'POST':
        form = RequestLoginForm(request.POST)
        print('is valid', form.is_valid())
        if form.is_valid() and form.cleaned_data['email'].endswith('@sussexstudent.com'):
            email_address = form.cleaned_data['email']
            try:
                user = FalmerUser.objects.get(identifier=email_address)
            except FalmerUser.DoesNotExist:
                user = FalmerUser.objects.create(
                    identifier=email_address,
                    authority='IS',
                )

            link = create_magic_link_for_user(user, '')
            send_mail(
                'Log in to Falmer',
                'Hi there! \n'
                'To login to Falmer, just follow the link below:\n'
                '{}{}\n\n'
                '- the website 🎉'.format(settings.PUBLIC_HOST, link),
                'website@sussexstudent.com',
                [email_address],
                html_message='Hi there!<br />'
                'To login to Falmer, just follow the link below:<br />'
                '<a href="{}{}">Log in to Falmer</a><br/><br/>'
                '- the website 🎉'.format(settings.PUBLIC_HOST, link),

            )

            return redirect('auth-request-sent')
    else:
        form = RequestLoginForm()
    return render(request, 'auth/link_request.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('/')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_jwt(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)

    return JsonResponse({
        'token': token,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return JsonResponse(MeSerializer(request.user).data)
