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

    @staticmethod
    def unpack_dict(dictionary):
        for key, value in dictionary.items():
            return value

    # TODO: updating not adding users
    def update(self, instance, validated_data):
        new_instances = validated_data.get('user')
        try:
            for inst in new_instances:
                instance.user.clear()
                instance.user.add(self.unpack_dict(inst))
            instance.save()
            return instance
        except TypeError:
            pass
