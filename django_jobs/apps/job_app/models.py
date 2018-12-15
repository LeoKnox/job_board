from __future__ import unicode_literals

from django.db import models
import bcrypt, re

class HelperManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["fname"]) < 3:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData["lname"]) < 3:
            errors["lname"] = "Last name should be at least 2 characters"
        if postData["password"] != postData["confirmpass"]:
            errors["passwords"] = "Passwords must match"
        if postData["password"] < 9:
            errors["password"] = "Password must be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["snail"] = "Invalid Email"
        check = Helper.objects.filter(email=postData["email"])
        if len(check)>0:
            errors["duplicate"] = "Email in use, please choose another"
        return errors
    
    def pw_validator(self, postData):
        errors = {}
        check = Helper.objects.filter(email=postData["email"])
        if len(check)>0:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            hpd = check[0].password
            if not EMAIL_REGEX.match(postData["email"]):
                errors["snail"] = "Invalid Email"
            if not bcrypt.checkpw(postData["password"].encode(), hpd.encode()):
                errors["login"] = "Incorrect user/password"
        else:
            errors["hail"] = "Try another Email"
        return errors

    def job_validator(self, postData):
        errord = {}
        if len(postData["ndescription"]) < 3:
            errord["description"] = "Description must be at least 3 characters"
        if len(postData["nlocation"])<3:
            errord["location"] = "Location must be at least 3 characters"
        return errord


# Create your models here.
class Helper(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = HelperManager()

class Job(models.Model):
    job=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    creator=models.ForeignKey(Helper, related_name="helper_id")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
