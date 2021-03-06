from statistics import mode
from django.db import models

class Invoice(models.Model):
    name = models.CharField(max_length=50)
    rfc = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    outdoor_number = models.IntegerField()
    interior_number = models.IntegerField()
    suburb = models.CharField(max_length=100)
    cp = models.BigIntegerField()
    municipality = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField()
    cell_phone_number = models.BigIntegerField()
    way_pay = models.CharField(max_length=100)
    bill_usage = models.CharField(max_length=250)
    regime = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name