from django.db import models
from django.core.validators import RegexValidator

from parks.models import Park

class Driver(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    YaId = models.CharField(max_length=200, unique=True)
    balance = models.FloatField(default=0.0)
    limit_1H = models.FloatField(default=0.0)
    limit_24H = models.FloatField(default=0.0)
    minimum = models.FloatField(default=0.0)
    
    # next 2 rows get from https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    parks = models.ForeignKey(Park, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.last_name