from django.urls import path

from drivers.views import *

urlpatterns = [
    path('all-drivers/', all_drivers_from_base, name='all-drivers'),
]