from rest_framework import serializers
from .models import Cutout, MoldStatistics, PlotterStatistics


class CutoutGetSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()
    created_date = serializers.DateTimeField(format="%d %b, %Y - %Ih %Mm %S %p")


class CutoutPostSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        cutout = Cutout.objects.create(**validated_data)
        return cutout


class MoldSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()

    def create(self, validated_data):
        plotter_id = validated_data.get('plotter_id')
        mold_id = validated_data.get('mold_id')
        cutout_amounts = Cutout.objects.filter(mold=mold_id, plotter=plotter_id)
        result = 0
        for cutout_amount in cutout_amounts.all():
            result += cutout_amount.amount
        MoldStatistics.objects.filter(mold=mold_id, plotter=plotter_id).delete()
        cutout, _ = MoldStatistics.objects.get_or_create(**validated_data, cutouts=result)
        return cutout


class MoldGetSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    mold_id = serializers.IntegerField()
    cutouts = serializers.IntegerField()


class PlotterSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()

    def create(self, validated_data):
        plotter_id = validated_data.get('plotter_id')
        cutout_amounts = Cutout.objects.filter(plotter=plotter_id)
        result = 0
        for cutout_amount in cutout_amounts.all():
            result += cutout_amount.amount
        PlotterStatistics.objects.filter(plotter=plotter_id).delete()
        statistics, _ = PlotterStatistics.objects.get_or_create(**validated_data, cutouts=result)
        return statistics

class PlotterGetSerializer(serializers.Serializer):
    plotter_id = serializers.IntegerField()
    ip = serializers.IPAddressField()
    cutouts = serializers.IntegerField()
    last_cutout_date = serializers.DateField()
