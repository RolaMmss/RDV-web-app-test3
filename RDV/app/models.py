from django.db import models
from django.contrib.auth.models import User
# from datetime import date
from django.core.exceptions import ValidationError


# Create your models here.


# class Coach(models.Model):
#     name = models.CharField(max_length=100)
    
    
class Appointment(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    subject = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def clean(self):
        if self.date.weekday() in [5, 6]:
            raise ValidationError(
                ('Appointments cannot be scheduled on weekends.'),
                code='invalid'
            )
    
 
    
class AppointmentSession(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)
