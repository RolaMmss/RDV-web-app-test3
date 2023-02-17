from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.conf import settings
from django.views.generic import View, ListView
from .models import Appointment, AppointmentSession
from .forms import AppointmentForm, LoginForm, SignupForm, NoteForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.db import models




# Create your views here.

# @login_required

def homepage(request):
    """ View function that renders the homepage template.
    Parameters:
        request: the HTTP request object.

    Returns:
        A rendered HTTP response with the homepage template.
    """   
    return render (request, "app/homepage.html")
####################################################""
def login_page(request):
    """The function login_page takes a request object and renders the login.html template with a LoginForm instance and a message. If the request method is POST, the form is validated and the user is authenticated using the provided username and password. If the authentication is successful, the user is logged in and redirected to the home page. Otherwise, an error message is displayed.
        The coach is staff and may sign in with:
            Username: Dr.Django
            Password: passworddjango
    Parameters:
        request: the HTTP request object sent by the client.

    Returns: 
        HttpResponse object that represents the rendered response of the login.html template.
    """
    form = LoginForm()
    message= ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
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
def signup_page(request):
    """Create a signup page view for the app.

    Args:
        request (HttpRequest): The HTTP request.
    
    Returns:
        HttpResponse: The HTTP response with the rendered signup page.    """
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('home')
    return render(request, 'app/signup.html', context={'form': form})
# ##############################################
def logout_user(request):
    """Log out the currently authenticated user and redirect them to the login page.

    Args:
        request: The HTTP request object.
    Returns:
        A redirect response to the login page.
    """
    logout(request)
    return redirect('login')
#################################################
def book_appointment(request):
    """This function takes a request as an argument and renders the 'book_appointment.html' template with a form to book a new appointment. 
    Args:
        request: A HttpRequest object representing the incoming request.

    Returns:
        A rendered template with a form to book a new appointment. 
    """
    form = AppointmentForm()
    message = ''
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            message = 'Date format : YY/MM/DD'
            start_time = form.cleaned_data['start_time']
            date = form.cleaned_data['date']
            subject = request.POST.get('subject')
            
            # Check for existing appointment with the same date and time
            existing_appointment = Appointment.objects.filter(start_time=start_time, date=date)
            if existing_appointment.exists():
                messages.error(request, 'Appointment already exists for this date and time.')
            else:   
                # save the appointment
                appointment = Appointment.objects.create(
                    start_time=start_time,
                    subject=subject,
                    date= date,
                    user = request.user
                    )
                return redirect('home')
                messages.success(request, 'Appointment has been booked successfully')
    return render(request, 'app/book_appointment.html', context={'user': User, "form":form})
###############################################################""
# class RendezVousListView(ListView):
#     model = AppointmentSession
#     template_name = 'appointment_list.html'

#     def get_queryset(self):
#         client_id = self.kwargs['client_id']
#         return AppointmentSession.objects.filter(client_id=client_id)  
# ###############################################################

# def appointment_session_view(request):
#     appointment_sessions = AppointmentSession.objects.all()
#     context = {'appointment_sessions': appointment_sessions}
#     return render(request, 'app/appointment_list.html', context)


def appointment_session_view(request):
    """Renders a view for appointment session displaying to users or staff based on authentication status.

    Args:
        request: HTTP request object

    Returns:
        A rendered view of appointment sessions in the template 'app/appointment_list.html' containing all appointment objects for staff or only the objects for the current user.
    """
    if request.user.is_staff:
        appointment_sessions = Appointment.objects.all().order_by('date','start_time')
    else:
        appointment_sessions = Appointment.objects.filter(user=request.user).order_by('date','start_time')
    context = {'appointment_sessions': appointment_sessions}
    return render(request, 'app/appointment_list.html', context)

###########################################################
# def add_note(request, appointment_id):
#     """The add_note function takes a request and appointment_id as input parameters. It retrieves an appointment object with the provided appointment_id and updates its note field with the note retrieved from the POST data. 

#     Args:
#         request : HTTP request object containing metadata about the request
#         appointment_id : ID of the appointment to be updated

#     Returns:
#         Redirects to the appointment_session_view page if the user is not a staff user, or redirects to the same page with updated appointment data if the note is successfully added. If the request method is not POST, renders a template with the appointment and note data.
#     """
#     appointment = get_object_or_404(Appointment, id=appointment_id)

#     # Check if the user is a staff user
#     if not request.user.is_staff:
#         return redirect('appointment_session_view')

#     if request.method == 'POST':
#         # Retrieve the note from the POST data
#         note = request.POST.get('note')

#         # Update the note field of the appointment object
#         appointment.note = note

#         # Save the updated appointment object to the database
#         appointment.save()

#         return redirect('appointment_session_view')

#     # If the request method is not POST, render a template with the appointment and note data
#     context = {'appointment': appointment}
#     return render(request, 'app/add_note.html', context)
#######################################################################

def note(request):
    """Create a note view 

    Args:
        request (HttpRequest): The HTTP request.
    
    Returns:
        HttpResponse: The HTTP response with the rendered signup page.    """
    form = NoteForm()
    if request.method == 'POST':
        # Retrieve the note from the POST data
        form = NoteForm(request.POST)
        if form.is_valid():
            note = request.POST.get('note')
        
            # Update the note field of the appointment object
            appointment.note = note
            # Save the updated appointment object to the database
            appointment.save()
            # If the request method is not POST, render a template with the appointment and note data
            return redirect('appointment_session_view')
    return render(request, 'app/note.html', context={'appointment': Appointment})