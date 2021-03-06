from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, \
    Permission
from django.conf import settings
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from falmer.slack.models import SlackUser

AUTHORITY_INTERNAL_STAFF = 'IS'

AUTHORITY_CHOICES = (
  ('IS', 'Internal Staff'),
  ('MSL', 'MSL Users'),
)


class FalmerUserManager(BaseUserManager):
    def _create_user(self, identifier, password,
                 is_staff, is_superuser, **extra_fields):
        if not identifier:
            raise ValueError('The given identifier must be set')
        user = self.model(identifier=identifier,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, identifier, **extra_fields):
        return self._create_user(identifier, '' ,False, False,
                             **extra_fields)

    def create_superuser(self, identifier, password, **extra_fields):
        return self._create_user(identifier, password, True, True,
                             **extra_fields)

    def get_or_create_msl_user(self, verified_payload):
        user, created = self.get_or_create(authority='MSL', identifier=verified_payload['uniqueid'], defaults={
            'name': f"{verified_payload['firstname']} {verified_payload['lastname']}"
        })

        if created:
            students = Group.objects.get(name='Students')
            students.user_set.add(user)

        return user


class FalmerUser(AbstractBaseUser, PermissionsMixin):
    identifier = models.CharField(max_length=256, unique=True)
    password = models.CharField(_('password'), max_length=128, default='', blank=True)
    authority = models.CharField(max_length=4, choices=AUTHORITY_CHOICES, )
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=128, default='', blank=True)
    USERNAME_FIELD = 'identifier'

    objects = FalmerUserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.get_full_name()

    def name_or_email(self):
        return self.name or self.email or self.identifier

    def __str__(self):
        return f'User: "{self.authority}/{self.identifier}"'

    def get_permissions(self):
        if self.is_superuser:
            permissions = Permission.objects.all()
        else:
            permissions = Permission.objects.filter(Q(user=self) | Q(group__user=self)).all()

        return set([p.pk for p in permissions])

    def ensure_ambient_permissions(self):
        if self.identifier.endswith('@sussexstudent.com'):
            try:
                group = Group.objects.get(name='Staff')
                self.groups.add(group)
            except Group.DoesNotExist:
                pass

        if self.identifier.endswith('@societies.sussexstudent.com'):
            try:
                group = Group.objects.get(name='Societies')
                self.groups.add(group)
            except Group.DoesNotExist:
                pass


class MagicLinkToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    @staticmethod
    def create_for_user(user):
        token = get_random_string(24)
        return MagicLinkToken.objects.create(user=user, token=token)

