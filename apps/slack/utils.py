from django.conf import settings
from slacker import Slacker


def get_slacker_instance():
    return Slacker(settings.SLACK_API_KEY)


def verify_slack_hook(func):
    def verify(*args, **kwargs):
        return func(*args, **kwargs)

    return verify
