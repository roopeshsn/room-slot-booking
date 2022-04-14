from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from base.models import Room, Booking, User, TimeSlot

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'email', 'name', 'is_active', 'staff', 'admin']


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'