from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from rooms.models import Room


class RoomSerializer(ModelSerializer):
    # get name instead of ids
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = '__all__'
