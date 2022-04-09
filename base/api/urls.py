from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('users/', views.getUsers),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    path('bookings/', views.getBookings),
]