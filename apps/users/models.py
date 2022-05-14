from statistics import mode
from django.db import models
from apps.invoices.models import Invoice

class Users(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    cp = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    municipality = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    cell_phone_number = models.BigIntegerField(null=True, blank=True)
    company_institution = models.CharField(max_length=50, null=True, blank=True)
    specialty = models.CharField(max_length=50, null=True, blank=True)
    professional_license = models.CharField(max_length=255, null=True, blank=True)
    specialty_certificate = models.CharField(max_length=255, null=True, blank=True)
    price_pay = models.BigIntegerField(null=True, default=0)
    
    invoice = models.ForeignKey(
        Invoice, 
        on_delete=models.CASCADE, 
        null=True
    )
    
    def get_full_name(self) -> str:
        return '{} {}'.format(self.name, self.last_name)
    
    def __str__(self) -> str:
        return self.get_full_name()
    
class QR(models.Model):
    text = models.CharField(max_length=50)
    qr = models.ImageField(upload_to='qr/')