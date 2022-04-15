from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm, TimeSlotForm, RegisterForm, UserUpdateForm
from .models import Room, Booking, TimeSlot
from datetime import datetime, date, timedelta

User = get_user_model()


# home page view
def home(request):
    return render(request, 'base/home.html')

# signin page view
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
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

# signup page view
def signupPage(request):
    page = 'signup'
    form = RegisterForm()
    context = {'page': page, 'form': form}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred!')

    return render(request, 'base/login_register.html', context)

# signout page view
def signoutUser(request):
    logout(request)
    return redirect('signin')

# For Users
# dashboard page view
@login_required(redirect_field_name='/signin')
def dashboard(request):
    today = datetime.now()
    default_date = today.strftime("%Y-%m-%d")
    if request.method == 'POST':
        picked_date = str(request.POST['date'])
        f_date = picked_date.replace('-', '')
        return redirect('available-rooms', f_date)
    context = {'today': default_date}
    return render(request, 'base/dashboard.html', context)

# available rooms page view
@login_required(redirect_field_name='/signin')
def availableRooms(request, date):
    f_date = datetime.strptime(date, "%Y%m%d").date().strftime("%Y-%m-%d")
    rooms = Room.objects.all()
    context = {'rooms': rooms, 'date': date}
    return render(request, 'base/available_rooms.html', context)

# available timeslots page view
@login_required(redirect_field_name='/signin')
def availableTimeSlots(request, date, pk):
    room = Room.objects.get(id=pk)
    time_slots = TimeSlot.objects.filter(room=room)
    context = {'time_slots': time_slots, 'room': room, 'date': date}
    return render(request, 'base/available_timeslots.html', context)

# user profile page view
@login_required(redirect_field_name='/signin')
def userProfile(request):
    user = User.objects.get(email=request.user)
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully!')
        else:
            form = UserUpdateForm(instance=user)
    context = {'form': form}
    return render(request, 'base/profile.html', context)

# room page view
@login_required(redirect_field_name='/signin')
def room(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room': room_object}
    return render(request, 'base/room.html', context)

# book room page view
# booking logic
@login_required(redirect_field_name='/signin')
def bookRoom(request, p_date, pk):
    f_date = datetime.strptime(p_date, "%Y%m%d").date().strftime("%Y-%m-%d")
    user = User.objects.get(email=request.user)
    time_slot = TimeSlot.objects.get(id=pk)
    days = time_slot.room.advance_booking

    picked_date_obj = datetime.strptime(f_date, "%Y-%m-%d")
    # calc_date_obj = date.today() + timedelta(days=days)
    today_date_obj = date.today()
    
    try:
        booking_obj = Booking.objects.filter(user=user, time_slot=time_slot)
    except:
        print("Queryset doesnot exists")

    if booking_obj.exists():
        message = 'ALREADY YOU'
    elif time_slot.booked == True:
        message = 'ALREADY'
    elif (picked_date_obj.day - today_date_obj.day >= days) and (time_slot.booked == False):
        TimeSlot.objects.filter(id=pk).update(booked=True)
        Booking.objects.create(user=user, time_slot=time_slot, date=f_date)
        message = 'SUCCESS'
    elif not((picked_date_obj.day - today_date_obj.day >= days) and (time_slot.booked == False)):
        message = 'FAILURE'
    elif not(picked_date_obj.day >= today_date_obj.day):
        message = 'ERROR'
    else:
        message = 'ERROR'

    context = {'user': user, 'time_slot': time_slot, 'message': message, 'days': days}
    return render(request, 'base/book_room.html', context)

# cancel booking page view
@login_required(redirect_field_name='/signin')
def cancelRoom(request, ts, pk):
    booking = Booking.objects.filter(id=pk)

    if request.method == 'POST':
        booking.delete()
        TimeSlot.objects.filter(id=ts).update(booked=False)
        return redirect('user-bookings')
    
    context = {'booking': booking}
    return render(request, 'base/cancel_room.html', context)

# For Room Manager
# manage page view
@staff_member_required
def manage(request):
    return render(request, 'base/manage.html')

# Rooms
# add rooms page view
@staff_member_required
def addRooms(request):
    form = RoomForm()
    current_user = request.user

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-rooms')

    return render(request, 'base/add_rooms.html', {'form': form, 'user': current_user})

# view rooms page view
@staff_member_required
def viewRooms(request):
    rooms = Room.objects.all()
    total_rooms = len(rooms)

    context = {'rooms': rooms, 'total_rooms': total_rooms}
    return render(request, 'base/view_rooms.html', context)

# update room page view
@staff_member_required
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

# delete room page view
@staff_member_required
def deleteRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
        context = {'room': room}
    except:
        context = {'error': 'An error occured!'}

    if request.method == 'POST':
        room.delete()
        return redirect('view-rooms')

    return render(request, 'base/delete.html', context)

# Timeslots
# add timeslots for a room page view
@staff_member_required
def addTimeSlots(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    if request.method == 'POST':
        check_in_time = request.POST['check_in_time']
        check_out_time = request.POST['check_out_time']
        TimeSlot.objects.create(check_in_time=check_in_time, check_out_time=check_out_time, room=room)
        return redirect('view-timeslots', room.id)
    
    return render(request, 'base/add_timeslots.html', context)

# view timeslots page view
@staff_member_required
def viewTimeSlots(request, pk):
    room = Room.objects.get(id=pk)
    time_slots = TimeSlot.objects.filter(room=room)

    context = {'time_slots': time_slots, 'room': room}
    return render(request, 'base/view_timeslots.html', context)

# delete timeslot page view
@staff_member_required
def deleteTimeSlot(request, pk):
    try:
        time_slot =TimeSlot.objects.get(id=pk)
        room = time_slot.room
        context = {'time_slot': time_slot}
    except:
        context = {'error': 'An error occured!'}

    if request.method == 'POST':
        time_slot.delete()
        return redirect('view-timeslots', room.id)

    return render(request, 'base/delete_timeslot.html', context)

# Bookings
# view bookings page view
@staff_member_required
def viewBookings(request):
    all_bookings = Booking.objects.all()

    context = {'bookings': all_bookings}
    return render(request, 'base/bookings.html', context)

# view user bookings page view
@login_required(redirect_field_name='/signin')
def userBookings(request):
    user = User.objects.get(email=request.user)
    bookings = Booking.objects.filter(user=user)
    context = {'user': user, 'bookings': bookings}

    return render(request, 'base/user_bookings.html', context)