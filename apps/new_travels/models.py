
# Create your models here.
from __future__ import unicode_literals

from django.db import models
from datetime import date, datetime
from time import strptime
import md5
import bcrypt
import os, binascii


# Create your models here.
class UserManager(models.Manager):
    def login(self, postData):
        messages = []
        # name = postData['name']
        # if len(str(name)) < 3:
        #     messages.append("Name must be at least 3 characters long!")
        username = postData['username']
        if len(str(username)) < 1:
            messages.append("username must not be blank!")
        if len(str(username)) < 3:
            messages.append("username must be at least 3 characters long!")
        password = postData['password']
        if len(str(password)) < 1:
            messages.append("password must not be blank")
        if len(str(password)) < 8:
            messages.append("password must be at least 8 characters long!")
        if User.objects.filter(username=username):
            # encode the password to a specific format since the above email is registered
            login_pw = password.encode()
            # encode the registered user's password from database to a specific format
            db_pw = User.objects.get(username=username).password.encode()
            # compare the password with the password in database
            if not bcrypt.checkpw(login_pw, db_pw):
                messages.append("Password is Incorrect!")
        else:
            messages.append("Username has already been registered!")
        return messages

    def register(self, postData):
        print "register process"
        messages = []
        name = postData['name']
        if len(str(name)) < 1:
            messages.append("Error! Name must not be blank!")
        if len(str(name)) < 2:
            messages.append("Error! Name must be at least 2 characters long!")

        # last_name = postData['last_name']
        # if len(str(last_name)) < 1:
        #     messages.append("Error! Last name must not be blank!")
        # if len(str(last_name)) < 2:
        #     messages.append("Error! Last name must be at least 2 characters long!")

        # alias = postData['alias']
        # if len(str(alias)) < 1:
        #     messages.append("Error! Alias must not be blank!")
        # if len(str(alias)) < 2:
        #     messages.append("Error! Alias must be at least 2 characters long!")

        username = postData['username']
        if len(str(username)) < 1:
            messages.append("Error! Username must not be blank!")
        if len(str(username)) < 2:
            messages.append("Error! Username must be at least 2 characters long!")

        password = postData['password']
        if len(str(password)) < 1:
            messages.append("Error! Password must not be blank!")
        if len(str(password)) < 8:
            messages.append("Error! Password must be at least 8 characters long!")

        pw_confirm = postData['pw_confirm']
        if pw_confirm != password:
            messages.append("Error! Passwords must match!")

        user_list = User.objects.filter(username=username)
        for user in user_list:
            print user.name
        if user_list:
            messages.append("Error! Username is already in the system!")
        if not messages:
            print "No messages"
            password = password.encode()
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password, salt)
            # password = password
            print "Create User"
            print hashed_pw
            User.objects.create(name=name, username=username, password=hashed_pw)
            print hashed_pw
            print User.objects.all()
            return None
        return messages

class TripManager(models.Manager):
    def validate(self, postData, id):
        messages = []
        destination = postData['destination']
        if len(str(destination)) > 0:
            messages.append("Travel Destination Must Not Be Blank")
        else:
            messages.append("Travel Destination Added")
        description = postData['description']
        if len(str(description)) > 0:
            messages.append("Travel Description Must Not Be Blank")
        start_date = postData['start_date']
        if str(date.today()) > str(start_date):
            messages.append("Trip must be started in the future, bruh!")
        end_date = postData['end_date']
        if str(end_date) < str(start_date):
            messages.append("Trip cannot go back in time!")
        if len(messages) > 0:
            self.create(destination=destination, description=description, start_date=start_date, end_date=end_date, planner=User.objects.get(id=id)
            )
            return messages
        else:
            messages.append("Error, your trip was not added")
            return messages

    def join(self, id, travel_id):
        joiner = User.get(id=id)
        plan = self.get(travel_id=id)
        plan.join.add(joiner)
        messages.append("Success! Trip joined!")

class User(models.Model):
    name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", Name: " + str(self.name) + ", Username: " + str(self.username) + ", Password: " + str(self.password)

class Trip(models.Model):
    destination = models.CharField(max_length = 50)
    description = models.CharField(max_length = 140)
    start_date = models.DateField()
    end_date = models.DateField()
    planner = models.ForeignKey(User, related_name='trip')
    travelers = models.ManyToManyField(User, related_name='trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", Destination: " + str(self.destination) + ", Description: " + str(self.description) + ", Start Date: " + str(self.start_date) + ", End Date: " + str(self.end_date) + ", Planner: " + str(self.planner)
