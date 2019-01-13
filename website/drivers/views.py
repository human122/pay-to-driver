from django.shortcuts import render
from django.http import HttpResponse

from .models import Driver

def all_drivers_from_yandex(request):
    pass

def all_drivers_from_base(request):
    drivers = Driver.objects.all()
    # print(type(drivers))
    # d = list(drivers)
    return render(request, 'drivers_from_base.html', context={'drivers': drivers})
    # HttpResponse(d)