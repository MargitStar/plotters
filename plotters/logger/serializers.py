from rest_framework import serializers
from .models import Cutout, MoldStatistics


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


class MoldSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()

    def create(self, validated_data):
        plotter_id = validated_data.get('plotter_id')
        mold_id = validated_data.get('mold_id')
        cutout_amount = len(
            Cutout.objects.filter(mold=mold_id, plotter=plotter_id))
        MoldStatistics.objects.filter(mold=mold_id, plotter=plotter_id).delete()
        cutout, _ = MoldStatistics.objects.get_or_create(**validated_data, cutouts=cutout_amount)

        return cutout
