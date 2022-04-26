from statistics import mode
from django.db import models

from apps.courses.models import Course

class Users(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    cp = models.IntegerField()
    state = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    cell_phone_number = models.BigIntegerField(null=True)
    company_institution = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    professional_license = models.CharField(max_length=255)
    specialty_certificate = models.CharField(max_length=255)
    price_pay = models.BigIntegerField(null=True)
    
    course_pre = models.ForeignKey(
        Course, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='%(app_label)s_%(class)s_related_pre'
    )
    course_trans = models.ForeignKey(
        Course, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='%(app_label)s_%(class)s_related_trans'
    )
    
    def get_full_name(self) -> str:
        return '{} {}'.format(self.name, self.last_name)
    
    def __str__(self) -> str:
        return self.get_full_name()