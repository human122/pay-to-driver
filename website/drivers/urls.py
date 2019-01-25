from django.urls import path

from drivers.views import *

urlpatterns = [
    path('all-drivers/', all_drivers_from_base, name='all-drivers'),
    path('one-driver/<int:pk>/', driver_from_yandex, name='one-driver'),
    path('one-driver/<int:pk>/detail/', driver_detail, name='driver-detail'),    
]