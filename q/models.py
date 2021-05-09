from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta, date
from time import strptime

import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z -]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z -]+$')
        
        
        

        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should have at least 2 characters.'
        elif not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = 'First name must consist of only letters'
        
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should have at least 2 characters.'
        elif not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = 'Last name must consist of only letters and space or dash characters'

        
        if len(post_data['email']) < 1:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Please enter a valid email address'
        
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if post_data['password'] != post_data['pw_confirm']:
            errors['password'] = 'Passwords must match'

        return errors
    def quote_validator(self, postData):
        

        errors={}
        if len(postData['author']) < 2:
            errors['author'] = "Person should have at least 2 letters in his name"

        if len(postData['message']) < 10:
            errors['message'] = "Message should have at least 10 characters"
        
       
        
        
        return errors

        

    

class User(models.Model):
    first_name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    email = models.CharField(max_length = 64)
    password = models.CharField(max_length = 64)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()





class Quote(models.Model):
    author = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    quoter = models.ForeignKey(User, related_name="quoters", on_delete=models.CASCADE)
    user_who_like = models.ManyToManyField(User, related_name="liked_quote")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
   
