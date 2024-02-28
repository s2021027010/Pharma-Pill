from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
import sys , os

from . import views 

from django.urls import include, path
from django.conf.urls import include

urlpatterns = [
    path('home/' , views.home, name='home'), 
    path('medicine/' , views.medicine, name='medicine'),
    path('profile/' , views.profile, name='profile'),
    path('update_Profile/' , views.update_Profile, name='update_Profile'),
    path('adminControl/' , views.admin_control, name='admin_control'),
    path('addMedicine/' , views.add_Medicine, name='add_Medicine'),
    path('deleteMedicine/<str:id>/' , views.delete_Medicine, name='delete_Medicine'),
    path('updateMedicine/' , views.update_Medicine, name='update_Medicine'),
    path('AddImgMedicine/' , views.AddImg_Medicine, name='AddImg_Medicine'),
    path('cart_list/' , views.cart_list, name='cart_list'),
    path('bill_report/' , views.bill_report, name='bill_report'),
    path('search/' , views.search, name='search'),   
    path('optionAdd/' , views.optionAdd, name='optionAdd'),
    path('update_list_company/' , views.update_list_company, name='update_list_company'),
    path('update_list_type/' , views.update_list_type, name='update_list_type'),
    path('setting/' , views.setting, name='setting'),
    path('admin_dataTable/' , views.admin_dataTable, name='admin_dataTable'),
    path('order_status/' , views.order_status, name='order_status'),
    path('order_delete_admin/<str:id>/' , views.order_delete_admin, name='order_delete_admin'),
    path('medicine_order/' , views.medicine_order, name='medicine_order'), 
    path('time_setting/' , views.time_setting, name='time_setting'),
    path('update_time_setting/<str:id>/' , views.update_time_setting, name='update_time_setting'),
    path('time_delete/<str:id>/' , views.time_delete, name='time_delete'),
    path('about_pharma/' , views.about_pharma, name='about_pharma'),
    path('delete_about/<str:id>/' , views.delete_about, name='delete_about'),
    path('blog_pharma/' , views.blog_pharma, name='blog_pharma'),
    path('delete_blog/' , views.delete_blog, name='delete_blog'),

    path('loader/' , views.loaderPage, name='loaderPage'),  # about_pharma
    path('header/' , views.header, name='header'),
    path('footer/' , views.footer, name='footer'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)