from rest_framework import serializers
from falmer.auth.models import FalmerUser


class MeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = FalmerUser
        fields = ('name', 'identifier')

    def get_name(self, model):
        return model.get_full_name()
