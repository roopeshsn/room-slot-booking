# Room Slot Booking

## FOSSEE Registration Details

Name: Roopesh Saravanan  
Email: helloiamroopesh@gmail.com  
Username (yaksh.fossee.in): heyroopesh

## Project Details

A Room Slot Booking Application, built using Python, Django, and Django REST Framework.

![HomePage Image](/static/screenshots/customer/1-HomePage.png)

View more [screenshots](/static/screenshots/)

## Setup

### Download Code and Run

1. Download and Extract the zip file of the project and cd into  
   `cd room-slot-booking-master`
   OR  
   `git clone https://github.com/roopeshsn/room-slot-booking.git`  
   `cd room-slot-booking`
2. Install virtualenv  
   `pip install virtualenv`  
   If you already installed virtualenv then skip this step.
3. Create Virtual Environment  
   `virtualenv venv`
4. Activate Virtual Environment  
   `venv\scripts\activate`
5. Install Dependencies  
   `pip install -r requirements.txt`
6. Run Server  
   `python manage.py runserver`
7. Run Tests  
   `python manage.py test`

## Highlights of the project

- PEP-8 standards followed.
- Built with Django and Django REST Framework.
- Test cases written.
- Django Template System used for rendering HTML pages (Frontend).
- API endpoints created for managing users, rooms, timeslots, and bookings.

## Details of the project

- A customer can book rooms on their preferred date and also they have option to cancel the booking.
- A customer can see their respective bookings.
- A Room manager can add, update or delete rooms and respected timeslots.
- A Room manager can view the bookings of the user.
- An Admin can assign the position "Staff", which means Room Manager to anyone who is signed up as a user.
- A demo database is created with users and rooms with respected timeslots
  1. Admin (superuser): email: "admin@admin.com", password: "admin123"
  2. Room Manager (staff): email: "manager@manager.com", password: "manager123"
  3. Customer1: email: "user1@user.com", password: "user1abc"
  4. Customer2: email: "user2@user.com", password: "user2abc"
