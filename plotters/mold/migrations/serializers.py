from rest_framework import serializers


class MoldSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
