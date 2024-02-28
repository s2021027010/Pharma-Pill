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
    path('logIn/' , views.logIn, name='lgIn'),
    path('signUp/' , views.signUp, name='register'), 
    path('logOut/', views.logOut, name='lgOut'), 
    path('forgotPass/' , views.forgotPass, name='forgotPass'),
    path('changePassword/' , views.changePassword, name='changePassword'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('verify/<auth_token>' , views.verify , name="verify"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)