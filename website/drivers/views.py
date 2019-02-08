from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

import requests

from .models import Driver
from parks.models import Park
from .config import YANDEX_API_KEY


def driver_from_yandex(request, slug):
    driver = get_object_or_404(Driver, YaId=slug)
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

@login_required(login_url='/drivers/login/')
def all_drivers_from_base(request):    
    drivers = Driver.objects.all()
    if request.method == 'POST':
        sync_db_with_remote()
    
    drivers_count = len(drivers)
    return render(request, 'drivers_from_base.html', {'drivers': drivers, 'count': drivers_count})

# TODO: refactor all this trash!!!!
def sync_db_with_remote():
    drivers = Driver.objects.all()
    r = requests.get(settings.GET_LIST_URL)
    b = requests.get(settings.GET_BALANCE_URL)
    param_list = []
    for i in range(len(drivers)):
        param_list.append(drivers[i].YaId)
        param_list.append(drivers[i].last_name)
        param_list.append(drivers[i].first_name)
        param_list.append(drivers[i].middle_name)
        param_list.append(drivers[i].phone_number)
        param_list.append(drivers[i].balance)

    drivers_id_from_db      = set(param_list[::6])
    drivers_id_from_remote  = set(b.json().keys())


    def del_from_db(drivers_id_from_db, drivers_id_from_remote):
        to_del = drivers_id_from_db - drivers_id_from_remote

        # see also https://stackoverflow.com/questions/5956391/django-objects-filter-with-list
        Driver.objects.filter(YaId__in=to_del).delete()


    def update_in_db(drivers_id_from_db, drivers_id_from_remote):
        gen = zip(param_list[1::6],
                  param_list[2::6],
                  param_list[3::6],
                  param_list[4::6],
                  param_list[5::6])
        for driver in drivers_id_from_db & drivers_id_from_remote:
            for ln, fn, mn, ph, bal in gen:
                if ln != r.json()['drivers'][driver].get('LastName'):
                    param_list[param_list.index(driver)+1] = r.json()['drivers'][driver].get('LastName')
                if fn != r.json()['drivers'][driver].get('FirstName'):
                    param_list[param_list.index(driver)+2] = r.json()['drivers'][driver].get('FirstName')
                if mn != r.json()['drivers'][driver].get('Surname'):
                    param_list[param_list.index(driver)+3] = r.json()['drivers'][driver].get('Surname')
                if ph != r.json()['drivers'][driver].get('Phones'):
                    param_list[param_list.index(driver)+4] = r.json()['drivers'][driver].get('Phones')
                if bal != b.json()[driver]:
                    param_list[param_list.index(driver)+5] = b.json()[driver]

    
    def add_new(drivers_id_from_db, drivers_id_from_remote):
        for driver in drivers_id_from_remote - drivers_id_from_db:
            param_list.append(driver)
            param_list.append(r.json()['drivers'][driver].get('LastName', ''))
            param_list.append(r.json()['drivers'][driver].get('FirstName', ''))
            param_list.append(r.json()['drivers'][driver].get('Surname', ''))
            param_list.append(r.json()['drivers'][driver].get('Phones', ''))
            param_list.append(b.json()[driver])

    print('hello before')
    update_in_db(drivers_id_from_db, drivers_id_from_remote)
    print('hello after')
    add_new(drivers_id_from_db, drivers_id_from_remote)

    for driver in param_list[::6]:
        if len(Driver.objects.filter(YaId=driver)) > 0:
            Driver.objects.filter(YaId=driver).last_name = param_list[param_list.index(driver)+1]
            Driver.objects.filter(YaId=driver).first_name = param_list[param_list.index(driver)+2]
            Driver.objects.filter(YaId=driver).middle_name = param_list[param_list.index(driver)+3]
            Driver.objects.filter(YaId=driver).phone_number = param_list[param_list.index(driver)+4]
            Driver.objects.filter(YaId=driver).balance = param_list[param_list.index(driver)+5]
        else:
            p = Park.objects.all()
            Driver.objects.create(
                                YaId=driver, 
                                last_name=param_list[param_list.index(driver)+1],
                                first_name=param_list[param_list.index(driver)+2],
                                middle_name=param_list[param_list.index(driver)+3],
                                phone_number=param_list[param_list.index(driver)+4],
                                balance=param_list[param_list.index(driver)+5],
                                parks=p[0]
                                )