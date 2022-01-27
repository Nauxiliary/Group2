from django.shortcuts import render
from common.models import Appointment
from django.views.generic import ListView


class AppointmentView(ListView):
    model = Appointment
    template_name = 'test_page.html'
# Create your views here.
