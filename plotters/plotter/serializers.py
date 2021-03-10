from rest_framework import serializers
from .models import Plotter, User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class PlotterSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=150)
    user = UserSerializer(many=True)

    def create(self, validated_data):
        user = validated_data.pop('user', [])
        plotter = Plotter.objects.create(**validated_data)

        for current in user:
            user_ = User.objects.get(pk=current.get('id'))
            plotter.user.add(user_)
        return plotter
