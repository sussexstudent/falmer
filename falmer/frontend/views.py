from django.http import Http404, HttpResponse
from django.template.context_processors import csrf
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from .models import FrontendDeployment

dev = """
<!doctype html>
<html lang="en">
  <head>
    <title>Loading | Falmer</title>
  </head>
  <body class="FalmerSite">
    <script type="text/javascript">window.CSRF = "{csrf_token}";</script>
    <div class="FalmerAppRoot"></div>
    <script type="text/javascript" src="http://localhost:8080/vendor.js"></script>
    <script type="text/javascript" src="http://localhost:8080/devFonts.js"></script>
    <script type="text/javascript" src="http://localhost:8080/main.js"></script>
    <script type="text/javascript" src="http://localhost:8080/productionFonts.js"></script>
  </body>
</html>
"""


def application_serve(request):
    if request.is_ajax() is False:
        try:
            deployment = FrontendDeployment.objects.filter(enabled=True).latest('created_at')
        except FrontendDeployment.DoesNotExist:
            return HttpResponse(dev.format(csrf_token=csrf(request)['csrf_token']))

        return HttpResponse(deployment.content.format(csrf_token=csrf(request)['csrf_token']))
    raise Http404()


class FrontendAPI(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [DjangoModelPermissions, ]
    queryset = FrontendDeployment.objects.none()

    def post(self, request):
        FrontendDeployment.objects.create(
            content=request.data['contents'],
        )
        return HttpResponse(status=200)
