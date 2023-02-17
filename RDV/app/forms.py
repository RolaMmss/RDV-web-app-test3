from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Appointment
from django.forms import ModelForm
from django.contrib.auth.models import User
import datetime
from datetime import date
from django.db import models




class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
#############################################
class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()         # la méthode utilitaire  get_user_model, qui vous permet d’obtenir le modèle  User sans l’importer directement
        fields = ('username', 'email', 'first_name', 'last_name')#, 'role')

##############################################
class AppointmentForm(forms.ModelForm):
    today = date.today
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': today}))
    start_times = [datetime.time(hour=9), datetime.time(hour=10), datetime.time(hour=11), datetime.time(hour=13),datetime.time(hour=14),datetime.time(hour=15),datetime.time(hour=16)]
    start_time = forms.TimeField(widget=forms.Select(choices=[(t.strftime('%H:%M'), t.strftime('%I:%M %p')) for t in start_times]))
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        date = cleaned_data.get('date')

     
    class Meta:
        model = Appointment
        fields = ['date', 'start_time', 'subject']
###################################################
class AppointmentSessionForm(forms.ModelForm):
    date = forms.DateField( required=False)
    start_time = forms.TimeField( required=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = forms.CharField(max_length=250)

#####################################################
class NoteForm(forms.ModelForm):
    note = forms.CharField(max_length=250)


