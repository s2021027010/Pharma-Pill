from asyncio.windows_events import NULL
from email.policy import default
from enum import auto
from datetime import datetime, time, date
from random import choices
from django.db import models
from django.contrib.auth.models import User


class db_Profile(models.Model):
    db_email = models.OneToOneField(User , on_delete = models.CASCADE)
    char_email = models.CharField(max_length = 255)
    db_gender = models.CharField(max_length = 125)
    db_address = models.TextField(max_length = 500)
    db_address_Country = models.TextField(max_length = 500)
    db_phoneNumber = models.CharField(max_length = 255)
    db_date_DoB = models.DateField(auto_now_add = False, auto_now = False, blank = True) 
    auth_token = models.CharField(max_length=100 ) 
    db_photo = models.ImageField(upload_to = "Profile/", width_field = None, height_field = None, max_length = 500, blank = True)  
    
    is_verified = models.BooleanField(default=False)  

    def __str__(self):
        return self.char_email
    def get_user_by_email(char_email):
        try:
            return db_Profile.objects.get(db_email = char_email)
        except:
            return False

    def isExists(self):
        if db_Profile.objects.filter(User = self.char_email):
            return True
        return False
 