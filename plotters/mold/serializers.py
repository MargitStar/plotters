from rest_framework import serializers
from .models import Mold


class MoldSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Mold.objects.create(**validated_data)
