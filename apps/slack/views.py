from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

from apps.auth.utils import create_magic_link_for_user
from apps.auth.models import FalmerUser
from .utils import verify_slack_hook, get_slacker_instance


@verify_slack_hook
def open_falmer(request):
    slack_user_id = request.POST.get('user_id')

    slack = get_slacker_instance()
    slack_profile = slack.users.profile.get(slack_user_id).body['profile']
    slack_user_email = slack_profile['email']

    try:
        user = FalmerUser.objects.get(identifier=slack_user_email, authority='IS')
    except FalmerUser.DoesNotExist:
        slack.chat.post_message(
            '#falmer', '<@{new_slack_id}> opened Falmer for the first time!'.format(new_slack_id=slack_user_id)
        )

        user = FalmerUser.objects.create(
            name='{} {}'.format(slack_profile['first_name'], slack_profile['last_name']),
            identifier=slack_user_email,
            authority='IS',
        )

    link = create_magic_link_for_user(user, '')

    return HttpResponse('Here\'s a magic link to login: {}{}'.format(settings.PUBLIC_HOST, link))

