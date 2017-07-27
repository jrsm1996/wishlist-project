from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validateLogin(self, form_data):
        errors = []
        if form_data['username'] < 3:
            errors.append('The username you entered is invalid.')
        else:
            user = User.objects.filter(username = form_data['username']).first()
            if user:
                password = str(form_data['password'])
                hashed_pw = bcrypt.hashpw(password, str(user.password))
                if hashed_pw != user.password:
                    errors.append('The password you entered is invalid.')
            else:
                errors.append('The username you entered is not in our database.')
        return errors

    def validateRegistration(self, form_data):
        errors = []
        if len(form_data['username']) < 3:
            errors.append('Please enter a username that is 3 or more characters.')
        else:
            user = User.objects.filter(username = form_data['username']).first()
            if user:
                errors.append('The username you entered has already been used to create an account. Please enter a different username.')
        if len(form_data['name']) < 3:
            errors.append('Please enter a name that is 3 or more characters.')
        if len(form_data['password']) < 8:
            errors.append('Please enter a password that is 8 or more characters')
        else:
            if form_data['password'] != form_data['confirm_password']:
                errors.append('The password and confirm password fields must match.')
        return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(
            name = form_data['name'],
            username = form_data['username'],
            created_at = form_data['date'],
            password = hashed_pw
        )
        return user

    def currentUser(self, request):
        return User.objects.get(id = request.session['user_id'])

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.CharField(max_length = 20)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length = 255)
    creator = models.ForeignKey(User, related_name = "created_items")
    users = models.ManyToManyField(User, related_name = "items")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
