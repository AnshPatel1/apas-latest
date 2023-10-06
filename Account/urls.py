from django.contrib import admin
from django.urls import path, include
from Account import views

urlpatterns = [
    path("login/", views.login),

]
