from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from base.forms import RoomForm, TimeSlotForm
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
    # Initial DB setup
    def setUp(self):
        self.room_a = Room.objects.create(name='room a', advance_booking=2, booked=False)
        self.room_b = Room.objects.create(name='room b', advance_booking=3, booked=False)

    # Testcase for queryset
    def test_queryset_exists(self):
        qs = Room.objects.all()
        self.assertTrue(qs.exists())

    # Testcase for valid room form
    def test_room_form(self):
        room_c = Room.objects.create(name='room c', advance_booking=1, booked=False)
        data = {'name': room_c.name, 'advance_booking': room_c.advance_booking,}
        form = RoomForm(data=data)
        self.assertTrue(form.is_valid())

    # Testcase for invalid room form
    def test_room_form_invalid(self):
        room_c = Room.objects.create(name='', advance_booking=1, booked=False)
        data = {'name': room_c.name, 'advance_booking': room_c.advance_booking,}
        form = RoomForm(data=data)
        self.assertFalse(form.is_valid())

# Test case for Timeslot Model
class TimeSlotTestCase(TestCase):
    # Initial DB setup
    def setUp(self):
        self.room_a = Room.objects.create(name='room a', advance_booking=2, booked=False)
        self.timeslot_a = TimeSlot.objects.create(check_in_time='13:00', check_out_time='15:00', room=self.room_a, booked=False)
    
    # Testcase for queryset
    def test_queryset_exists(self):
        qs = TimeSlot.objects.all()
        self.assertTrue(qs.exists())

    # Testcase for valid timeslot form
    def test_timeslot_form(self):
        data = {'check_in_time': self.timeslot_a.check_in_time, 'check_out_time': self.timeslot_a.check_out_time, 'room': self.room_a,}
        form = TimeSlotForm(data=data)
        self.assertTrue(form.is_valid())

    # Testcase for invalid valid timeslot form
    def test_timeslot_form_invalid(self):
        data = {'check_in_time': '', 'check_out_time': self.timeslot_a.check_out_time, 'room': self.room_a,}
        form = TimeSlotForm(data=data)
        self.assertFalse(form.is_valid())


# Test case for Booking Model
class BookingTestCase(TestCase):
    # Initial DB setup
    def setUp(self):
        self.user_a = User.objects.create(name='user a', email='usera@user.com', password='123')
        self.room_a = Room.objects.create(name='room a', advance_booking=2, booked=False)
        self.room_b = Room.objects.create(name='room b', advance_booking=1, booked=False)
        self.timeslot_a = TimeSlot.objects.create(check_in_time='12:00', check_out_time='18:00', room=self.room_a, booked=False)
        Booking.objects.create(user=self.user_a, time_slot=self.timeslot_a, date='2022-04-18')

    # Testcase for queryset
    def test_queryset_exists(self):
        qs = Booking.objects.all()
        self.assertTrue(qs.exists())