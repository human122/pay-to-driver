from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

import requests

from .models import Driver
from .config import YANDEX_API_KEY


def driver_from_yandex(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    r = requests.get(settings.GET_LIST_URL)
    if r.status_code == 200:
        if driver.YaId in r.json()['drivers'].keys():
            d = requests.get(settings.GET_DRIVER_URL + driver.YaId)
            if d.status_code == 200:
                check_list = 'first_name FirstName last_name LastName phone_number Phones'.split()
                if d.json()['balance'] != driver.balance:
                    driver.balance = d.json()['balance']                    
                for db, ya in zip(check_list[::2],check_list[1::2]):
                    if getattr(driver, db) != d.json()['driver'][ya]:
                        setattr(driver, db, d.json()['driver'][ya])
                driver.save() # TODO: call to db, is it needed in all cases?
                return render(request, 'one_driver.html', {'driver': driver})

        else:
            return HttpResponse("<h1>Водитель с таким id не найден в Яндекс</h1>")
    else:
        return HttpResponse("<h1>Яндекс не отвечает, попробуйте повторить запрос позже</h1>")

def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    return render(request, 'one-driver.html', {'driver': driver})

def all_drivers_from_base(request):    
    drivers = Driver.objects.all()
    # if request.POST[]
    return render(request, 'drivers_from_base.html', {'drivers': drivers})