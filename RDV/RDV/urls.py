"""RDV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from app import views
from app.views import * #homepage, login_page, signup_page, logout_user, book_appointment, appointment_session_view #RendezVousListView#, appointment_calendar, make_appointment, appointment_confirmation 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),  
    path('logout/',logout_user, name='logout'),
    path('book/', book_appointment, name='book_appointment'),
    path('list/', appointment_session_view, name='appointment_list'),
    path('note/<int:appointment_id>/', note, name='note'),

]   


