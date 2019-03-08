from django.db import models

from qiwi.models import Qiwi_Driver


class Payment(models.Model):
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)
    driver = models.ForeignKey(Qiwi_Driver, on_delete=models.CASCADE)

    def __str__(self):
        return 'date: {}, amount: {}, driver: {}'.format(
            self.date,
            self.amount,
            self.driver)
