from operator import mod
from xmlrpc.client import DateTime
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_manageruser(self, name, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin?"
        return self.admin
    
    objects = UserManager()

class Room(models.Model):
    name = models.CharField(max_length=30)
    advance_booking = models.IntegerField()
    booked = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.room.name


class TimeSlot(models.Model):
    check_in_time =  models.TimeField(max_length=4)
    check_out_time = models.TimeField(max_length=4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    
    # def __str__(self):
    #     return f'{self.user} has booked {self.room} from {self.room.defined_check_in_time} to {self.room.defined_check_out_time} on {self.room.date}'


