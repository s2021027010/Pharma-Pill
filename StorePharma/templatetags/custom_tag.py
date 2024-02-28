 
from django import template 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404 

from StorePharma.models import (db_Medicine, medicine_Image, med_Cart_list, med_Order )
from AuthenticApp.models import db_Profile
register = template.Library()

#{{view_Product.db_Product_ID|Review_count}}
#{{prod.db_Product_ID|email:user.email}}
# -------------------------------------------<< >>-------------------------------------------------------
'''
@register.filter
def wish_count(value):
    count = db_Medicine.objects.filter(db_Wishlist_email = value).all().count() 
    return count

@register.filter(name="email", is_safe=True)
def wishlist(ID, email):
    if med_Cart_list.objects.filter(db_Wishlist_ID = ID, db_Wishlist_email = email).first() :
        item = "heart_broken"
    else:
        item = "favorite" 
    return item
'''
@register.filter(name="email", is_safe=True)
def Cart_count(Pk_Cart, email):
    obj_cart_list = med_Cart_list.objects.filter(Pk_Cart_ID = Pk_Cart, cart_email = email).first()
    ID = obj_cart_list.med_Cart_ID 
    Quantity = med_Cart_list.objects.filter(cart_email = email, med_Cart_ID = ID, Pk_Cart_ID = Pk_Cart).aggregate(TOTAL = Sum("Med_Cart_Quantity"))['TOTAL']  
    price = db_Medicine.objects.filter(Medicine_ID = ID).aggregate(TOTAL = Sum("Med_Sell_Price"))['TOTAL']    

    Total_item = Quantity * price 
    return Total_item
@register.filter
def GetTotalPrice(value):
    obj_cart_list = med_Cart_list.objects.filter(Pk_Cart_ID = value).first()
    ID = obj_cart_list.med_Cart_ID 
    email = obj_cart_list.cart_email
    Quantity = med_Cart_list.objects.filter(cart_email = email, med_Cart_ID = ID, Pk_Cart_ID = value).aggregate(TOTAL = Sum("Med_Cart_Quantity"))['TOTAL']  
    price = db_Medicine.objects.filter(Medicine_ID = ID).aggregate(TOTAL = Sum("Med_Sell_Price"))['TOTAL']    

    Total_item = Quantity * price
    return Total_item

@register.filter(name="account", is_safe=True)
def order_report(cart_ID, order_ID):  
    if med_Order.objects.filter(med_order_ID = cart_ID, Pk_order_ID = order_ID).exists() == True:
        order_get_id = get_object_or_404(db_Medicine, Medicine_ID = cart_ID) 
        return order_get_id.Medicine_ID

@register.filter(name="admin", is_safe=True)
def order_report(cart_ID, order_ID):   
    if med_Order.objects.filter(med_order_ID = cart_ID, Pk_order_ID = order_ID).exists() == True: 
        order_get_id = get_object_or_404(db_Medicine, Medicine_ID = cart_ID)  
        return order_get_id.Medicine_ID

'''
@register.filter
def GetItem(ID):   
    obj_Order = med_Order.objects.filter(med_order_ID = ID, ).values_list()
    if obj_Order : 
        print(obj_Order)
    else:
        print("yes")
    return obj_Order
'''
@register.filter
def GetName(ID):
    obj_Med = db_Medicine.objects.filter(Medicine_ID = ID).first()
    name = obj_Med.Med_LabelName
    return name

@register.filter
def GetPrice(ID):
    obj_Med = db_Medicine.objects.filter(Medicine_ID = ID).first()
    price = obj_Med.Med_Sell_Price
    return price

@register.filter
def GetQuantity(ID):
    obj_Order = med_Cart_list.objects.filter(Pk_Cart_ID = ID).first()
    Quantity = obj_Order.Med_Cart_Quantity
    return Quantity

@register.filter
def totalUser_count(value):
    count = User.objects.filter().all().count() 
    return count
 

@register.filter
def ActiveUser_count(value):  
    count = db_Profile.objects.filter(is_verified = True).all().count()  
    return count

@register.filter
def total_item_count(value):
    count = db_Medicine.objects.filter().all().count() 
    return count

@register.filter
def total_Amount_count(value): 
    total_sum = 0 
    Total_item = 1
    for med in db_Medicine.objects.all():
        price = float(med.Med_Purchase_Price)
        Quantity = float(med.Med_Quantity) 
        if Quantity == 0:
            Total_item = 0
        else:
            Total_item = Quantity * price 
        total_sum = float(total_sum) + Total_item
    return total_sum


@register.filter
def orderPassed_count(value):
    count = med_Order.objects.filter(status_Cart = "Passed").all().count() 
    return count

@register.filter
def orderPending_count(value):
    count = med_Order.objects.filter(status_Cart = "Pendding").all().count() 
    return count

@register.filter
def orderWaiting_count(value):
    count = med_Order.objects.filter(status_Cart = "Waiting").all().count() 
    return count

@register.filter
def orderCancel_count(value):
    count = med_Order.objects.filter(status_Cart = "Cancel").all().count() 
    return count


@register.filter
def totalEarn_count(value):  
    price = med_Order.objects.filter(status_Cart = "Passed").aggregate(TOTAL = Sum("Med_Price"))['TOTAL']
    if price is None:
        price = 0
    return price
