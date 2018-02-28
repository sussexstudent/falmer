from rest_framework import views, serializers
from rest_framework.decorators import permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from falmer.content.serializers import WagtailImageSerializer
from falmer.matte.models import MatteImage


class MatteUploadSerializer(serializers.Serializer):
    source = serializers.IntegerField()
    file = serializers.FileField()

    def create(self, validated_data):
        image = MatteImage.objects.create(
            internal_source=validated_data['source'],
            file=validated_data['file'],
            file_size=validated_data['file'].size,
            uploaded_by_user=validated_data['user']
        )

        return image


class Image(views.APIView):
    # parser_classes = (FileUploadParser, )

    @permission_classes((IsAuthenticated,))
    def put(self, request):
        image = MatteUploadSerializer(data=request.data)

        if image.is_valid():
            image = image.save(user=request.user)

            return Response({
                'ok': True,
                'data': WagtailImageSerializer(instance=image).data
            }, status=200)
