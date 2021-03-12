from rest_framework import serializers
from .models import Cutout


class CutoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()
    created_date = serializers.DateTimeField(format="%d %b, %Y - %Ih %Mm %S %p")

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        plotter_id = validated_data.get('plotter_id')
        mold_id = validated_data.get('mold_id')
        created_date = validated_data.get('created_date')
        cutout = Cutout.objects.create(**validated_data)
        return cutout