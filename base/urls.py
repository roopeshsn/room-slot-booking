from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signinPage, name='signin'),
    path('signup/', views.signupPage, name='signup'),
    path('signout/', views.signoutUser, name='signout'),
    path('manage/', views.manage, name='manage'),
    path('dashboard/', views.dashboard, name='dashboard')
]