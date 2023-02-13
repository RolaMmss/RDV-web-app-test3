from django.db import models

# Create your models here.


class Coach(models.Model):
    name = models.CharField(max_length=100)
    
    
class Appointment(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    # date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # purpose = models.CharField(max_length=255)
    subject = models.CharField(max_length=200)
    