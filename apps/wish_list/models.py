from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class UserManager(models.Manager):
    def validReg(self, postData):
        errors = []
        if not postData['name'].isalpha():
            errors.append('Name can only contain alphabetical characters!')
        if len(postData['name']) < 3:
            errors.append('Name must be at least three letters!')
        if len(postData['username']) < 3:
            errors.append('username must be at least three characters!')
        if not postData['hired_at']:
            errors.append('Please fill out date form')
        if len(postData['password']) < 8:
            errors.append('Password must contain at least 8 characters!')
        if postData['password'] != postData['confirm']:
            errors.append('Passwords must match!')
        if User.objects.filter(username = postData['username']):
            errors.append('Username already exists.')
        return errors

class ItemManager(models.Manager):
    def validItem(self, postData):
        errors = []
        if len(postData['item']) < 3:
            errors.append('Item must contain at least three characters!')
        if User.objects.filter(name = postData['item']):
            errors.append('Item already exists.')
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    hired_at = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name='added_item')
    liked_by = models.ManyToManyField(User,related_name='liked_item')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()
