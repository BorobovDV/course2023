from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('billboard/', billboard, name='billboard'),
    path('date_selection/', date_selection, name='date_selection'),
    path('scheme/', scheme, name='scheme'),
    path('test/', test, name='test'),
    path('rent/', rent, name='rent'),
    path('deleteAllRents/', deleteAllRents, name='deleteAllRents'),
    path('auth/', auth, name='auth'),
    path('reg/', reg, name='reg'),
    path('q/', exit_acc, name='exit_acc'),
]
