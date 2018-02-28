import jwt

from falmer.auth.models import FalmerUser


class MSLJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            token = request.META['HTTP_AUTHORIZATION'][7:]
            if token != '':
                print(f'token "{token}"')
                decoded = jwt.decode(token, 'test', algorithms=['HS256'])

                user = FalmerUser.objects.get_or_create_msl_user(decoded)

                request.user = user
        except (KeyError, jwt.DecodeError) as e:
            print(e)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
