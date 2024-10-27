from django.contrib import admin
from django.urls import path, include
from compressor import views
from django.urls import path




from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.upload_image, name='upload_image'),
]
