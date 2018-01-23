from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from falmer.content.models import StaffMemberSnippet
from falmer.matte.models import MatteImage



def generate_image_url(image, filter_spec):
    from wagtail.wagtailimages.views.serve import generate_signature
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    # Append image's original filename to the URL (optional)
    # url += image.file.name[len('original_images/'):]

    return settings.PUBLIC_HOST + url


class WagtailImageSerializer(serializers.ModelSerializer):
    resource = serializers.SerializerMethodField()

    class Meta:
        model = MatteImage
        fields = ('id', 'resource', 'width', 'height')

    def get_resource(self, image):
        return image.file.name


class SnippetSerializer(serializers.ModelSerializer):
    photo = WagtailImageSerializer()

    class Meta:
        model = StaffMemberSnippet
        fields = ('name', 'job_title', 'email', 'office_phone_number', 'mobile_phone_number', 'job_description', 'office_location', 'photo')
