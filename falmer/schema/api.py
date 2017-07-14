from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.permissions import AllowAny
from wagtail.api.v2.endpoints import PagesAPIEndpoint as WagtailPagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.wagtailimages.api.v2.endpoints import ImagesAPIEndpoint
from wagtail.wagtaildocs.api.v2.endpoints import DocumentsAPIEndpoint
from .serializers import PageSerializer

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests


class BasePagesAPIEndpoint(WagtailPagesAPIEndpoint):
    required_scopes = ['read']

    base_serializer_class = PageSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    permission_classes = [AllowAny, ]

    body_fields = WagtailPagesAPIEndpoint.body_fields + [
    #    'guide',
    #    'content',
    #    'description'
    ]


api_router.register_endpoint('pages', BasePagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
api_router.register_endpoint('documents', DocumentsAPIEndpoint)
