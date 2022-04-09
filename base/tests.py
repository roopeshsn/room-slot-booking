from django.test import TestCase
from .models import Room, Booking, User

#Test case for User Model
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='test321@test.com', password='123')
    
    def test_queryset_exists(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())

# Test case for Room Model
class RoomTestCase(TestCase):
    def setUp(self):
        Room.objects.create(name='Room 23', date='2022-04-10', defined_check_in_time='12:00', defined_check_out_time='18:00', advance_booking=2, booked=False)

    def test_queryset_exists(self):
        qs = Room.objects.all()
        self.assertTrue(qs.exists())

# Test case for Booking Model
class BookingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='test321@test.com', password='123')
        self.room1 = Room.objects.create(name='Room 23', date='2022-04-10', defined_check_in_time='12:00', defined_check_out_time='18:00', advance_booking=2, booked=False)
        self.room2 = Room.objects.create(name='Room 25', date='2022-04-11', defined_check_in_time='13:00', defined_check_out_time='17:00', advance_booking=2, booked=False)
        Booking.objects.create(user=self.user1, room=self.room1)

    def test_queryset_exists(self):
        qs = Booking.objects.all()
        self.assertTrue(qs.exists())

    # def test_bookings_create(self):
    #     url = 'http://localhost:8000/book-room/{id}'.format(id = self.room2.id)
    #     response = self.client.post(url, {"date": '2020-03-16', "time_slot": '1'},headers={"Authorization": "token " + str(self.token2)})