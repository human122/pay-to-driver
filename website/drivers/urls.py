from django.urls import path
from django.contrib.auth import views as auth_views

from drivers.views import *

urlpatterns = [
    path('all-drivers/', all_drivers_from_base, name='all-drivers'),
    path('one-driver/<str:slug>/', driver_from_yandex, name='one-driver'),
    path('login/', auth_views.LoginView.as_view(
        template_name="login.html", 
        extra_context={'next': '/drivers/all-drivers/'}
        ), name="login"),
    path('logout/', auth_views.LogoutView.as_view(
        template_name="login.html",
        extra_context={'next': '/login/'}
        ), name='logout'),    
]