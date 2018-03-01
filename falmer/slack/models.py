from django.conf import settings
from django.db import models


class SlackUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='slack_account', on_delete=models.CASCADE)
    slack_user_id = models.CharField(max_length=12)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def has_name(self):
        return self.first_name != '' or self.last_name != ''
