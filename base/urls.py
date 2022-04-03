from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signinPage, name='signin'),
    path('signup/', views.signupPage, name='signup'),
    path('signout/', views.signoutUser, name='signout'),
    path('manage/', views.manage, name='manage'),
    path('manage/bookings', views.viewBookings, name='bookings'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('room/<str:pk>', views.room, name='room'),
    path('book-room/<str:pk>', views.bookRoom, name='book-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
]