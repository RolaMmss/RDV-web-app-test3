from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.conf import settings
from django.views.generic import View
from .models import Appointment, Coach
from .forms import AppointmentForm
from django.contrib import messages
import datetime
from django import forms


# Create your views here.
def homepage(request):
    # context = {
    # }
    return render (request, "app/homepage.html")
####################################################""
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'app/login.html', context={'form': form,'message':message})
################################################################
# class LoginPageView(View):
#     template_name = 'app/login.html'
#     form_class = forms.LoginForm

#     def get(self, request):
#         form = self.form_class()
#         message = ''
#         return render(request, self.template_name, context={'form': form, 'message': message})
        
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#         message = 'Identifiants invalides.'
#         return render(request, self.template_name, context={'form': form, 'message': message})
# ##############################################
def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('home')
    return render(request, 'app/signup.html', context={'form': form})
# ##############################################
def logout_user(request):
    
    logout(request)
    return redirect('login')
#################################################
# def appointment_calendar(request):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments/calendar.html', {'appointments': appointments})
# ##################################################
# def appointment_confirmation(request, appointment_id):
#     appointment = Appointment.objects.get(id=appointment_id)
#     return render(request, 'appointments/confirmation.html', {'appointment': appointment})
# #############################################
# def make_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             # Valider si le rendez-vous est possible en fonction des disponibilités
#             # et de la durée minimale entre les rendez-vous
#             if is_valid_appointment(appointment):
#                 appointment.save()
#                 return redirect('appointments:confirmation', appointment.id)
#     else:
#         form = AppointmentForm()
#     return render(request, 'appointments/make_appointment.html', {'form': form})
# ##########################################""
# def is_valid_appointment(appointment):
#     # Vérifier si le rendez-vous est possible en fonction des disponibilités
#     # et de la durée minimale entre les rendez-vous
#     return True

#################################################"""

def book_appointment(request):
    if request.method == 'POST':
        coach_id = request.POST.get('coach')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        subject = request.POST.get('subject')

        coach = Coach.objects.get(id=coach_id)
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        # vérifier si le coach est disponible
        is_coach_available = Appointment.objects.filter(coach=coach, start_time__range=(start_time, end_time)).exists() or \
                             Appointment.objects.filter(coach=coach, end_time__range=(start_time, end_time)).exists()
        if is_coach_available:
            messages.error(request, 'Coach is not available at this time')
            return redirect('book_appointment')

        # vérifier si il y a au moins 10 minutes entre deux rendez-vous
        last_appointment = Appointment.objects.filter(coach=coach, end_time__lt=start_time).last()
        if last_appointment and (start_time - last_appointment.end_time).total_seconds() / 60 < 10:
            messages.error(request, 'There should be at least 10 minutes gap between two appointments')
            return redirect('book_appointment')

        # vérifier si le temps de rendez-vous est entre 9h et 12h30 et de 13h30 à 17h
        if start_time.hour < 9 or start_time.hour >= 17 or \
           (start_time.hour == 12 and start_time.minute >= 30) or \
           (start_time.hour == 13 and start_time.minute < 30):
            messages.error(request, 'Appointment time should be between 9:00 and 12:30 and between 13:30 and 17:00')
            return redirect('book_appointment')

        # enregistrer le rendez-vous
        appointment = Appointment.objects.create(
            coach=coach,
            start_time=start_time,
            end_time=end_time,
            subject=subject
            )
        messages.success(request, 'Appointment has been booked successfully')
        return redirect('book_appointment')
    coaches = Coach.objects.all()
    context = {
        'coaches': coaches
    }
    return render(request, 'book_appointment.html', context)

# class BookAppointmentForm(forms.ModelForm):
#     coach = forms.ModelChoiceField(queryset=Coach.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
#     start_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     end_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))


class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['coach', 'start_time', 'end_time', 'subject']
        widgets = {
            'coach': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TextInput(attrs={'class': 'form-control'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'})
        }
