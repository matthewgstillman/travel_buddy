from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'new_travels/index.html')

def register(request):
    #print request.POST
    if request.method == 'POST':
        messages = User.objects.register(request.POST)
        #Above line might be postData
    if not messages:
        print "No messages! Success!"
        # fetch user id and name via email
        user_list = User.objects.all().filter(username=request.POST['username'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].name
        return redirect('/travels')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/')

def login(request):
    users = User.objects.all()
    postData = {
        'username': request.POST['username'],
        'password': request.POST['password'],
    }
    if request.method == 'POST':
        messages = User.objects.login(request.POST)
    if not messages:
        print "No messages! Success!"
        user_list = User.objects.all().filter(username=request.POST['username'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].name
        return redirect('/travels')
    else:
        request.session['messages'] = messages
        return redirect('/')

def travels(request):
    trips = Trip.objects.filter(planner__name=request.session['name'])
    other_trips = Trip.objects.exclude(planner__name=request.session['name'])
    print "Trips: ", trips
    context = {
        'trips': trips,
        'other_trips': other_trips
    }
    return render(request, 'new_travels/travels.html', context)

def destination(request, id):
    destination = Trip.objects.get(id=id)
    trips = Trip.objects.filter(planner__name=request.session['name'])
    trip_info = Trip.objects.all().filter(id=id)
    other_trips = Trip.objects.exclude(planner__name=request.session['name']).filter(id=id)
    print "Trip Info: ", trip_info
    context = {
        'trips': trips,
        'other_trips': other_trips,
        'destination': destination,
    }
    return render(request, 'new_travels/destination.html', context)

def add(request):
    return render(request, 'new_travels/add.html')

def join(request, travel_id):
    currentuser = User.objects.get(name=request.session['name'])
    other_trip = Trip.objects.get(id=id)
    other_trip.travelers.add(currentuser)
    travelers = other_trip.travelers.all()
    print "Travelers: ", travelers
    print "Current User: ", currentuser
    print "Other Trip: ", other_trip
    return redirect('/travels')

def add_trip(request):
    currentuser = request.session['id']
    print "Current User", currentuser
    # currenttrip = Trip.objects.filter(trip__id=id)
    print request.POST
    postData = {
        'destination': request.POST['destination'],
        'description': request.POST['description'],
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date']
    }
    messages = Trip.objects.validate(request.POST, currentuser)
    if not messages:
        print "Not messages! Success!"
    else:
        request.session['messages'] = messages
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')
