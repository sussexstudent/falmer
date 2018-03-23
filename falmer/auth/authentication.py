from django.conf import settings
from rest_framework import exceptions
import jwt

from falmer.auth.models import FalmerUser


class MSLJWTAuthentication:
    def authenticate(self, request):
        try:
            if request.META['HTTP_AUTHORIZATION'].startswith('Falmer '):
                return None

            token = request.META['HTTP_AUTHORIZATION'][7:]
            if token != '':
                decoded = jwt.decode(token, settings.MSL_JWT_SECRET, algorithms=['HS256'])

                user = FalmerUser.objects.get_or_create_msl_user(decoded)
                return user, None
        except KeyError as e:
            return None
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed('Token decode error')


    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format('Bearer ', 'api')
