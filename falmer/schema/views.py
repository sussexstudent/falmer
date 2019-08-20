from collections import namedtuple

import rest_framework
from promise import Promise
from promise.dataloader import DataLoader
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from graphene_django.views import GraphQLView

from falmer.events.models import EventLike

Context = namedtuple('Context', 'request loaders user site')
Loaders = namedtuple('Loaders', 'event_like')


class DRFAuthenticatedGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(GraphQLView, self).parse_body(request)

    def get_context(self, request):
        class EventLikeLoader(DataLoader):
            def batch_load_fn(self, keys):
                if request.user.is_authenticated:
                    likes = {event_like.event.id: event_like for event_like in EventLike.objects.filter(user=request.user, event__id__in=keys)}
                    return Promise.resolve([likes.get(event_id) for event_id in keys])
                else:
                    return Promise.resolve([None for event_id in keys])

        setattr(request, 'loaders', Loaders(event_like=EventLikeLoader()))
        return request
        #return Context(request=request, loaders=Loaders(event_like=EventLikeLoader()), user=request.user, site=request.site)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(GraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((AllowAny,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(['GET', 'POST'])(view)
        return view

