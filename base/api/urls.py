from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('users/', views.getUsers),
    path('users/<str:pk>/', views.getUser),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    path('timeslots/', views.getTimeSlots),
    path('timeslots/<str:pk>/', views.getTimeSlot),
    path('bookings/', views.getBookings),
]