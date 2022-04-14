from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from base.forms import RoomForm
from .models import Room, Booking, TimeSlot, User

#Test case for User Model
class UserTestCase(TestCase):
    def setUp(self):
        # Admin user
        user_a = User.objects.create(name='user_a', email='admin@admin.com', staff=True, admin=True)
        user_a_pw = '123'
        self.user_a_pw = user_a_pw
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        # Normal user
        user_b = User.objects.create(name='user_b', email='userb@user.com', staff=False, admin=False)
        user_b_pw = '1234'
        self.user_b_pw = user_b_pw
        user_b.set_password(user_b_pw)
        user_b.save()
        self.user_b = user_b
    
    def test_queryset_exists(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password(self.user_a_pw))

    def test_signin_url(self):
        signin_url = '/signin'
        data = {'email': self.user_a.email, 'password': self.user_a_pw}
        response = self.client.post(signin_url, data, follow=True)
        # print(dir(response))
        status_code = response.status_code
        # print(response.request.get('PATH_INFO'))
        self.assertEqual(status_code, 200)

    def test_valid_request(self):
        self.client.login(email=self.user_a.email, password=self.user_a_pw)
        response = self.client.post('/manage/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_request(self):
        self.client.login(email=self.user_b.email, password=self.user_b_pw)
        response = self.client.post('/manage/')
        self.assertNotEqual(response.status_code, 200)


# Test case for Room Model
class RoomTestCase(TestCase):
    def setUp(self):
        room_a = Room.objects.create(name='room a', advance_booking=2, booked=False)
        room_b = Room.objects.create(name='room b', advance_booking=3, booked=False)

    def test_queryset_exists(self):
        qs = Room.objects.all()
        self.assertTrue(qs.exists())

    # def test_create_room(self):
    #     room_c = Room.objects.create(name='room c', advance_booking=1, booked=False)
    #     self.assertTrue(room_c)

    def test_room_form(self):
        room_c = Room.objects.create(name='room c', advance_booking=1, booked=False)
        data = {'name': room_c.name, 'advance_booking': room_c.advance_booking,}
        form = RoomForm(data=data)
        self.assertTrue(form.is_valid())

    def test_room_form(self):
        room_c = Room.objects.create(name='', advance_booking=1, booked=False)
        data = {'name': room_c.name, 'advance_booking': room_c.advance_booking,}
        form = RoomForm(data=data)
        self.assertFalse(form.is_valid())
    

# Test case for Booking Model
class BookingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='test321@test.com', password='123')
        self.room1 = Room.objects.create(name='Room 23', advance_booking=2, booked=False)
        self.room2 = Room.objects.create(name='Room 25', advance_booking=2, booked=False)
        self.timeslot1 = TimeSlot.objects.create(check_in_time='12:00', check_out_time='18:00', room=self.room1, booked=False)
        Booking.objects.create(user=self.user1, time_slot=self.timeslot1, date='2022-04-17')

    def test_queryset_exists(self):
        qs = Booking.objects.all()
        self.assertTrue(qs.exists())