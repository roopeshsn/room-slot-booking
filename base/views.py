from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserAdminCreationForm, RoomForm
from .models import Room

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
def manage(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data.get('name')
            # date = form.cleaned_data.get('date')
            # defined_check_in_time = form.cleaned_data.get('defined_check_in_time')
            # defined_check_out_time = form.cleaned_data.get('defined_check_out_time')
            # room_object = Room(name=name, date=date, defined_check_in_time=defined_check_in_time, defined_check_out_time=defined_check_out_time)
            form.save()

    return render(request, 'base/manage.html', context)

def room(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room': room_object}
    return render(request, 'base/room.html', context)

@login_required(redirect_field_name='/signin')
def bookRoom(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room': room_object}
    return render(request, 'base/book_room.html', context)

def updateRoom(request, pk):
    room_object = Room.objects.get(id=pk)
    form = RoomForm(instance=room_object)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room_object)
        if form.is_valid():
            form.save()
    context = {'form': form,'room': room_object}
    return render(request, 'base/update_room.html', context)

def deleteRoom(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room': room_object}
    if request.method == 'POST':
        room_object.delete()
        return redirect('dashboard')
    return render(request, 'base/delete.html', context)