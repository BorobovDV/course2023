
from django.urls import path

from .views import *
urlpatterns = [
    path("auth/", auth, name='authentication'),
    path("reg/", reg, name='registration'),
]
