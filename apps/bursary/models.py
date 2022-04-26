from django.db import models

class Bursary(models.Model):
    code = models.CharField(max_length=10)
    invited_by = models.CharField(max_length=255, null=True)
    
    isActive = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.code