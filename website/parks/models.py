from django.db import models

class Park(models.Model):
    api_key = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    commission = models.IntegerField(default=0)
    is_active = models.BooleanField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
