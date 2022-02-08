from django.shortcuts import render, redirect
from common.models import Appointment
from django.views.generic import CreateView, ListView
from django.contrib import messages


class AppointmentView(CreateView):
    model = Appointment
    template_name = 'appointments.html'
    fields = ['request_date']


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments.html'
    fields = ['request_date']
# Create your views here.


def index_view(request):
    return render(request, 'index.html')


def make_appointment(request_date):
    return Appointment.objects.create(date=request_date)


def appointment(request):
    if request.method == "POST":
        form = Appointment(request.POST)

        if request.user.is_authenticated:

            if form.is_valid():
                obj = form.save(commit=False)
                obj.client = Appointment.objects.get(pk=request.user.id)
                obj.save()
            else:
                print("ERROR : Form is invalid")
                print(form.errors)

    return redirect('mainhome')
