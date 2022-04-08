from urllib import robotparser
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserAdminCreationForm, RoomForm, UserAdminChangeForm
from .models import Room, Booking

User = get_user_model()

def home(request):
    return render(request, 'base/home.html')

def signinPage(request):
    page = 'signin'
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request, 'User doesnot exist!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password doesnot exist!')

    print(request)
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def signupPage(request):
    page = 'signup'
    form = UserAdminCreationForm()
    context = {'page': page, 'form': form}

    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred!')

    return render(request, 'base/login_register.html', context)

def signoutUser(request):
    logout(request)
    return redirect('signin')

@login_required(redirect_field_name='/signin')
def dashboard(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/dashboard.html', context)

@login_required(redirect_field_name='/signin')
def userProfile(request):
    user = User.objects.get(email=request.user)
    form = UserAdminChangeForm(instance=user)
    context = {'form': form}
    return render(request, 'base/profile.html', context)

@login_required(redirect_field_name='/signin')
def manage(request):
    return render(request, 'base/manage.html')

@login_required(redirect_field_name='/signin')
def addRooms(request):
    form = RoomForm()
    current_user = request.user
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data.get('name')
            # date = form.cleaned_data.get('date')
            # defined_check_in_time = form.cleaned_data.get('defined_check_in_time')
            # defined_check_out_time = form.cleaned_data.get('defined_check_out_time')
            # room_object = Room(name=name, date=date, defined_check_in_time=defined_check_in_time, defined_check_out_time=defined_check_out_time)
            form.save()
            return redirect('dashboard')

    return render(request, 'base/manage_rooms.html', {'form': form, 'user': current_user})

@login_required(redirect_field_name='/signin')
def viewRooms(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/view_rooms.html', context)

@login_required(redirect_field_name='/signin')
def viewBookings(request):
    all_bookings = Booking.objects.all()
    print(all_bookings)
    context = {'bookings': all_bookings}
    return render(request, 'base/bookings.html', context)

@login_required(redirect_field_name='/signin')
def room(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room': room_object}
    return render(request, 'base/room.html', context)

@login_required(redirect_field_name='/signin')
def bookRoom(request, pk):
    status = False
    message = 'Room was already booked!'
    user_object = User.objects.get(email=request.user)
    room_object = Room.objects.get(id=pk)
    booking_object = Booking.objects.filter(user=user_object, room=room_object)

    if room_object.booked == False:
        Room.objects.filter(id=pk).update(booked=True)
        Booking.objects.create(user=user_object, room=room_object)
        message = 'Room booked successfully!'
        status = True
    elif booking_object:
        message = 'You already booked the room!'
        status = True
    else:
        message = 'Room was already booked!'
        status = False

    context = {'user': user_object, 'room': room_object, 'status': status, 'message': message}
    return render(request, 'base/book_room.html', context)

@login_required(redirect_field_name='/signin')
def cancelRoom(request, pk):
    user_object = User.objects.get(email=request.user)
    room_object = Room.objects.get(id=pk)
    booking_object = Booking.objects.filter(user=user_object, room=room_object)
    if request.method == 'POST':
        booking_object.delete()
        Room.objects.filter(id=pk).update(booked=False)
        return redirect('dashboard')
    context = {'booking': booking_object}
    return render(request, 'base/cancel_room.html', context)

@login_required(redirect_field_name='/signin')
def updateRoom(request, pk):
    room_object = Room.objects.get(id=pk)
    form = RoomForm(instance=room_object)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room_object)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form,'room': room_object}
    return render(request, 'base/update_room.html', context)

@login_required(redirect_field_name='/signin')
def deleteRoom(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room': room_object}
    if request.method == 'POST':
        room_object.delete()
        return redirect('view-rooms')
    return render(request, 'base/delete.html', context)

@login_required(redirect_field_name='/signin')
def userBookings(request):
    user_object = User.objects.get(email=request.user.email)
    booking_object = Booking.objects.filter(user=user_object)
    context = {'user': user_object, 'bookings': booking_object}

    return render(request, 'base/user_bookings.html', context)