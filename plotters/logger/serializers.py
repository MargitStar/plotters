from rest_framework import serializers
from .models import Cutout



class CutoutGetSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()
    created_date = serializers.DateTimeField(format="%d %b, %Y - %Ih %Mm %S %p")


class CutoutPostSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()

    def create(self, validated_data):
        plotter_id = serializers.IntegerField()
        mold_id = serializers.IntegerField()

        cutout = Cutout.objects.create(**validated_data)
        return cutout
