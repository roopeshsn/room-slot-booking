from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signinPage, name='signin'),
    path('signup/', views.signupPage, name='signup'),
    path('signout/', views.signoutUser, name='signout'),
    path('manage/', views.manage, name='manage'),
    path('manage/rooms', views.viewRooms, name='view-rooms'),
    path('manage/rooms/add', views.addRooms, name='add-rooms'),
    path('manage/bookings', views.viewBookings, name='bookings'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('room/<str:pk>', views.room, name='room'),
    path('user/bookings', views.userBookings, name='user-bookings'),
    path('user/profile', views.userProfile, name='user-profile'),
    path('book-room/<str:pk>', views.bookRoom, name='book-room'),
    path('cancel-room/<str:pk>', views.cancelRoom, name='cancel-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
]