from django.contrib import admin
from django.urls import include, path

from .views import register

urlpatterns = [
    path('', register, name="registration"),
]
