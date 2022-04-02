from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserAdminCreationForm

# Create your views here.

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
    return render(request, 'base/dashboard.html')

def manage(request):
    return render(request, 'base/manage.html')

# if user == User.objects.get(email=user)