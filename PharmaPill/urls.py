"""
URL configuration for PharmaPill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('Auth/', include('AuthenticApp.urls')),
    path('store/', include('StorePharma.urls')),
    path('admin/', admin.site.urls),
]

admin.site.site_header = "Pharma Pill"
admin.site.site_title = "Phama Pill"
admin.site.index_title = "Welcome to PHARMA Pill"