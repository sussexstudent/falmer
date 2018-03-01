from django.db import models

class MailChimpList(models.Model):
    class Meta:
        verbose_name = 'MailChimp List'

    mailchimp_list_id = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.slug


class NewsletterResumeToken(models.Model):
    list = models.ForeignKey(MailChimpList, on_delete=models.CASCADE)
    email_id = models.CharField(max_length=255)
    continuation_token = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
