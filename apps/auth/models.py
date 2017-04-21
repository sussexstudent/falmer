from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils.crypto import get_random_string

AUTHORITY_INTERNAL_STAFF = 'IS'

AUTHORITY_CHOICES = (
  ('IS', 'Internal Staff'),
)


class FalmerUserManager(BaseUserManager):
    def _create_user(self, identifier,
                 is_staff, is_superuser, **extra_fields):
        if not identifier:
            raise ValueError('The given username must be set')
        user = self.model(identifier=identifier,
                          is_staff=is_staff, is_active=True,
                          authority='IS',
                          is_superuser=is_superuser, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                             **extra_fields)

    def create_superuser(self, identifier, **extra_fields):
        return self._create_user(identifier, True, True,
                             **extra_fields)


class FalmerUser(AbstractBaseUser, PermissionsMixin):
    identifier = models.CharField(max_length=256, unique=True)
    authority = models.CharField(max_length=4, choices=AUTHORITY_CHOICES)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=128, default='', blank=True)
    USERNAME_FIELD = 'identifier'

    objects = FalmerUserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class MagicLinkToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    @staticmethod
    def create_for_user(user):
        token = get_random_string(24)
        return MagicLinkToken.objects.create(user=user, token=token)

