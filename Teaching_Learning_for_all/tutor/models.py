from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from datetime import datetime
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # PASS tests whether a field matches the pattern            
            errors.append ("Invalid email address!")

        if len(postData['first_name']) < 2:
            errors.append("First name should be at least 2 characters long ")

        if len(postData['last_name']) < 2:
            errors.append("Last name should be at least 2 characters long ")

        if len(postData['email']) < 1:    #pass email cant be blank 
            errors.append("Invalid Email")
        
        if len(postData['psw']) < 8:  
           errors.append("Your password needs to be at least 8 characters long")
        
        if postData['psw'] != postData['confirm']:      #PASS if password does not match 
            errors.append("Password does not match!")

        result = User.objects.filter(email = postData['email']) #PASS if the email already exists!
        if result:
            errors.append("Email already created!")


        else:                                                                   #PASS if younger than 13
            bd = datetime.strptime(postData['bday'],'%Y-%m-%d')
            today = datetime.now()
            if (bd.year +13, bd.month, bd.day) > (today.year, today.month, today.day):
               errors.append('User must be at least 13 years old to register')

            return errors

class CourseManager(models.Manager):
    def basic_validator(self, postData):
        errors = []
        result = Class.objects.filter(name = postData['name'])

        if len(postData['name']) < 5:
            errors.append("Title should be at least 5 characters")
        if len(postData['desc']) < 15:
            errors.append("Description needs to be at least 15 characters")
        if result:
            errors.append('This course is already created!')

        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 55)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 255)
    image = models.ImageField(default = "profile.jpeg")
    password = models.CharField(max_length = 255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Class(models.Model):
    name = models.CharField(max_length = 255)
    desc = models.TextField(max_length=450) # user who uploaded a specific book!
    tutor = models.ForeignKey(User, related_name ="classes_tutored", on_delete=models.CASCADE) # users who takes a specific course!
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CourseManager()


class WallMessage(models.Model):
    message = models.TextField(max_length=450)
    creator = models.ForeignKey(User, related_name = "user_messages", on_delete= models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name= "user_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField(max_length= 300)
    wall_message = models.ForeignKey(WallMessage, related_name="post_comments", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name.last_name} Profile'


