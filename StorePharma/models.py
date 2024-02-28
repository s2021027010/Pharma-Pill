from asyncio.windows_events import NULL
from email.policy import default
from enum import auto
from datetime import datetime, time, date
from random import choices
import django
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class db_Medicine(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Medicine_ID =  models.CharField(primary_key = True ,max_length = 100 )
    Med_LabelName = models.TextField(max_length = 500)
    Med_CompanyName = models.TextField(max_length = 500)
    Med_FormulaName = models.TextField(max_length = 500)
    Med_Purchase_Price = models.FloatField()
    Med_Sell_Price = models.FloatField()
    Med_Type = models.TextField(max_length = 500)  #{tablet, Syrup etc.}
    Med_UsedFor  = models.TextField(max_length = 1000)
    Med_Describtion = models.TextField(max_length = 1000)
    Med_ProductionDate  = models.DateField(auto_now_add = False, auto_now = False, blank = True)
    Med_ExpireDate  = models.DateField(auto_now_add = False, auto_now = False, blank = True)  
    Med_photo = models.ImageField(upload_to = "Medicine/", width_field = None, height_field = None, max_length = 255, blank = True) 
    
    Med_Status = models.TextField(max_length = 500)
    Med_Size = models.TextField(max_length = 500) # ml, mg ,mm , cc
    Med_Quantity = models.IntegerField() 
    Med_Remain_Quantity = models.IntegerField() 

    created_at = models.DateTimeField(auto_now_add = True) 
    
    def __str__(self):
        return self.Medicine_ID + " , " + self.Med_LabelName 
    def get_user_by_email(Med_ID):
        try:
            return db_Medicine.objects.get(Medicine_ID = Med_ID)
        except:
            return False
        
class medicine_Image(models.Model):
    Med_ID_Img =  models.CharField(max_length=100)
    list1_img =  models.ImageField(upload_to = "MedList/", width_field=None, height_field=None, max_length=255, blank=True) 
    list2_img =  models.ImageField(upload_to = "MedList/", width_field=None, height_field=None, max_length=255, blank=True)
    list3_img =  models.ImageField(upload_to = "MedList/", width_field=None, height_field=None, max_length=255, blank=True)
    list4_img =  models.ImageField(upload_to = "MedList/", width_field=None, height_field=None, max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.Med_ID_Img
    def get_med_by_email(Med_ID):
        try:
            return medicine_Image.objects.get(Med_ID_Img = Med_ID)
        except:
            return False

class med_Cart_list(models.Model):
    Pk_Cart_ID = models.CharField(primary_key = True, max_length = 100 )
    cart_email = models.CharField(max_length=255)
    med_Cart_ID = models.CharField(max_length = 100)
    Med_Cart_Quantity = models.IntegerField(default = 0)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.cart_email + " , " + self.med_Cart_ID
    def get_cart_by_email(cart_email):
        try:
            return med_Cart_list.objects.get(cart_email = cart_email)
        except:
            return False
 
class med_Order(models.Model):
    Pk_order_ID = models.CharField(primary_key = True, max_length = 100)
    order_email = models.CharField(max_length=255)
    med_order_ID = models.ManyToManyField(db_Medicine, default = True) 
    status_Cart = models.TextField(max_length = 100)
    Med_Price = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add = False, auto_now = False, blank = True, default = django.utils.timezone.now)
    # created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.order_email + ", " + self.Pk_order_ID
    def get_order_by_email(order_email):
        try:
            return med_Order.objects.get(order_email = order_email)
        except:
            return False
class med_OrderMedicine(models.Model):
    Pk_OrderMedicine_ID = models.CharField(primary_key = True, max_length = 100)
    order_OrderMedicine_ID = models.CharField(max_length = 100) 
    med_OrderMedicine_email = models.CharField(max_length=255)
    med_OrderMedicine_ID = models.CharField(max_length=255)
    Pk_Cart_List_ID = models.CharField(max_length=255)
    def __str__(self):
        return self.Pk_OrderMedicine_ID + ", " + self.order_OrderMedicine_ID
        
class OptionList(models.Model):
    Option_ID =  models.CharField(primary_key = True, max_length = 100)
    company_List = models.TextField(max_length = 255)
    type_List = models.TextField(max_length = 255)

class Pharma_TimeTable(models.Model):
    Pk_Time_ID = models.CharField(primary_key = True, max_length = 100 )
    DateFrom = models.CharField(max_length = 100)
    DateTo = models.CharField(max_length = 100)
    TimeFromHour = models.CharField(max_length = 100)
    TimeFromMin = models.CharField(max_length = 100)
    TimeToHour = models.CharField(max_length = 100)
    TimeToMin = models.CharField(max_length = 100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Pk_Time_ID
        
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   Company setting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class about_Pharma(models.Model):
    Pk_about_ID = models.CharField(primary_key = True, max_length = 100 )
    about_Title = models.TextField(max_length = 255)
    about_Describe = models.TextField(max_length = 1000) 
    about_admin_email = models.TextField(max_length = 255)
    about_address = models.TextField(max_length = 255)
    about_contact = models.TextField(max_length = 255)
    about_img =  models.ImageField(upload_to = "Profile/", width_field=None, height_field=None, max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Pk_about_ID + ", " + self.about_Title

class Blogs_Pharma(models.Model):
    Pk_blog_ID = models.CharField(primary_key = True, max_length = 100 )
    blog_Title = models.TextField(max_length = 255)
    blog_Medicine_Name = models.TextField(max_length = 255)
    blog_Describe = models.TextField(max_length = 1000)
    blog_img =  models.ImageField(upload_to = "Profile/", width_field=None, height_field=None, max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.Pk_blog_ID + ", " + self.blog_Title
