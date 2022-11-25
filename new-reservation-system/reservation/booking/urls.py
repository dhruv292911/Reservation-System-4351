from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),                   # name of the function is home from the views.py (views.home)
    path('registration', views.registration, name="registration"),
    path('reservation', views.reservation, name="reservation"),
    path('login', views.login, name="login"),
]
