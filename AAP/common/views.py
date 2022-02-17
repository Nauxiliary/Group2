from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import requestAppointmentForm, addPetForm
from accounts.models import User
from common.models import Appointment
from django.views.generic import ListView


def index_view(request):
    return render(request, 'index.html')


@login_required()
def request_appointment_view(request):
    if request.method == "POST":
        form = requestAppointmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = User.objects.get(pk=request.user.id)
            obj.status = 0
            obj.save()
            messages.success(request, "Appointment request sent successfully.")
            return redirect('appointments')
        else:
            messages.error(request, "Something went wrong. Request not sent.")
    else:
        form = requestAppointmentForm()

    return render(request, 'appointments.html', {'form': form})

@login_required()
class AppointmentView(ListView):
    model = Appointment
    template_name = 'appointments.html'


@login_required()
def add_pet_view(request):
    if request.method == "POST":
        form = addPetForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = User.objects.get(pk=request.user.id)
            obj.status = 0
            obj.save()
            messages.success(request, "Pet added.")
            return redirect('appointments')
        else:
            messages.error(request, "Something went wrong. Request not sent.")
    else:
        form = addPetForm()

    return render(request, 'petregister.html', {'form': form})
