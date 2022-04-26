from statistics import mode
from django.db import models

class CoursesPay(models.Model):
    id = models.IntegerField(primary_key=True)
    persons = models.IntegerField()
    
    def __str__(self) -> str:
        return 'Course {}'.format(self.id)
    
class CategoryCourse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(CategoryCourse, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    extra_cost = models.BigIntegerField()
    
    def __str__(self) -> str:
        return self.text