from django.db import models

# const prices = [
#     { 
#         id: 1, 
#         type: 'MÉDICOS ORTOPEDISTAS', 
#         price: 2500, 
#         valid: 'HASTA EL 30 DE MAYO', 
#         starting: 'A PARTIR DEL 30 DE MAYO', 
#         future_price: 3000,
#     },
#     { 
#         id: 2, 
#         type: 'MÉDICOS GENERALES, ENFERMERIA Y RESIDENTES', 
#         price: 1500, 
#         valid: 'HASTA EL 30 DE MAYO', 
#         starting: 'A PARTIR DEL 30 DE MAYO', 
#         future_price: 2000,
#     },
#     { 
#         id: 3, 
#         type: 'ACOMPAÑANTE', 
#         price: 2000, 
#         valid: 'HASTA EL 30 DE MAYO', 
#         starting: 'A PARTIR DEL 30 DE MAYO', 
#         future_price: 2500,
#     }
# ]

class Prices(models.Model):
    type = models.CharField(max_length=50)
    price = models.IntegerField()
    valid = models.DateField()
    starting = models.DateField()
    future_price = models.IntegerField()
    offer_expiration = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.type