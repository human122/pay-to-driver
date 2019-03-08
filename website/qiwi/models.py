from django.db import models

from parks.models import Park
from drivers.models import Driver


class Qiwi_Park(models.Model):
    amount = models.FloatField(default=0.0)
    updated = models.DateTimeField(auto_now=True)
    park = models.ForeignKey(Park, on_delete=models.CASCADE)

    # login =
    # password =

    def __str__(self):
        return '{} - {}'.format(self.park, self.amount)


class Qiwi_Driver(models.Model):
    amount = models.FloatField(default=0.0)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # account = driver.phone_number

    def __str__(self):
        return '{} - {}'.format(self.driver, self.amount)
