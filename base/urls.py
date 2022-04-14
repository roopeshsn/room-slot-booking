from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # api
    path('api/', include('base.api.urls')),
    # user actions
    path('signin/', views.signinPage, name='signin'),
    path('signup/', views.signupPage, name='signup'),
    path('signout/', views.signoutUser, name='signout'),
    # room manager actions
    path('manage/', views.manage, name='manage'),
    path('manage/rooms', views.viewRooms, name='view-rooms'),
    path('manage/rooms/add', views.addRooms, name='add-rooms'),
    path('manage/bookings', views.viewBookings, name='bookings'),
    path('manage/time-slots/<str:pk>', views.viewTimeSlots, name='view-timeslots'),
    path('manage/time-slots/add/<str:pk>', views.addTimeSlots, name='add-timeslots'),
    path('delete-timeslot/<str:pk>', views.deleteTimeSlot, name='delete-timeslot'),
    # user actions
    path('dashboard/', views.dashboard, name='dashboard'),
    path('available-rooms/<str:date>', views.availableRooms, name='available-rooms'),
    path('available-timeslots/<str:date>/<str:pk>', views.availableTimeSlots, name='available-timeslots'),
    path('room/<str:pk>', views.room, name='room'),
    path('user/bookings', views.userBookings, name='user-bookings'),
    path('user/profile', views.userProfile, name='user-profile'),
    path('book-room/<str:p_date>/<str:pk>', views.bookRoom, name='book-room'),
    path('cancel-room/<str:ts>/<str:pk>', views.cancelRoom, name='cancel-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
]