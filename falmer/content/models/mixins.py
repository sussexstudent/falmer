from django.db import models


class SocialMediaMixin(models.Model):
    class Meta:
        abstract = True

    social_facebook_url = models.URLField(blank=True, default='')
    social_twitter_handle = models.CharField(max_length=128, blank=True, default='')
    social_snapchat_handle = models.CharField(max_length=128, blank=True, default='')
    social_instagram_handle = models.CharField(max_length=128, blank=True, default='')
    social_email_address = models.EmailField(blank=True, default='')
