from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from base.models import Room, Booking, User

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'