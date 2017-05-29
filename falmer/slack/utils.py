from django.conf import settings
from django.http import JsonResponse
from slacker import Slacker


def get_slacker_instance():
    return Slacker(settings.SLACK_API_KEY)


def verify_slack_hook(func):
    def verify(*args, **kwargs):
        request_token = args[0].POST['token']
        if request_token != settings.SLACK_VERIFICATION_TOKEN:
            return JsonResponse({'error': 'slack verification incorrect'}, status=418)
        return func(*args, **kwargs)

    return verify
