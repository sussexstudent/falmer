import hmac
import hashlib
import base64
import binascii
from django.conf import settings
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.postgres.fields import JSONField
from falmer.core.models import TimeStampedModel


class ConsentCodeForm(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = AutoSlugField(populate_from='title', blank=False, null=False, unique=True)
    body = models.TextField(null=False, default='')
    hash_code = models.CharField(max_length=32, blank=False, null=False)
    additional_data = JSONField(blank=True)

    def __str__(self):
        return self.title


    def accept_for(self, user):
        if user is None:
            return None

        try:
            auth = ConsentCodeAuthorisation.objects.get(form=self, user=user)
            return auth
        except ConsentCodeAuthorisation.DoesNotExist:
            code_digest = hmac.digest(bytes(self.hash_code, 'utf-8'), str(user.pk).encode(), hashlib.sha256)
            short_code = binascii.hexlify(code_digest).decode('utf-8')[:12]
            print(short_code)

            auth = ConsentCodeAuthorisation()
            auth.form = self
            auth.user = user
            auth.code = short_code
            auth.additional_data = {}
            auth.save()

            return auth

class ConsentCodeAuthorisation(TimeStampedModel, models.Model):
    class Meta:
        unique_together = ('user', 'form')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='consent')
    form = models.ForeignKey(ConsentCodeForm, on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=12)

    additional_data = JSONField(blank=True)

    def __str__(self):
        return '{user} / {form}'.format(user=self.user.name, form=self.form.title)
