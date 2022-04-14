from os import times
from sqlite3 import Timestamp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Booking, User, TimeSlot
from .serializers import RoomSerializer, TimeSlotSerializer, UserSerializer, BookingSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/users',
        'GET /api/rooms',
        'GET /api/room/:id',
        'GET /api/timeslots',
        'GET /api/timeslots/:id',
        'GET /api/bookings',
        'GET /api/bookings/:id',
    ]
    return Response(routes)

# user model
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# Room Model
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)

# Timeslot model
@api_view(['GET'])
def getTimeSlots(request):
    timeslots = TimeSlot.objects.all()
    serializer = TimeSlotSerializer(timeslots, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTimeSlot(request, pk):
    timeslot = TimeSlot.objects.get(id=pk)
    serializer = TimeSlotSerializer(timeslot, many=False)
    return Response(serializer.data)

# booking model
@api_view(['GET'])
def getBookings(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    serializer = BookingSerializer(booking, many=False)
    return Response(serializer.data)