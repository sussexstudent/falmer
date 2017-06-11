from rest_framework import serializers

from falmer.content.serializers import WagtailImageSerializer
from falmer.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    featured_image = WagtailImageSerializer()

    class Meta:
        model = Event
        fields = ('social_facebook', 'smart_location', 'featured_image')
