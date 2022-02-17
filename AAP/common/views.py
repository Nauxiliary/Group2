from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import requestAppointmentForm, addPetForm
from accounts.models import User
from django.views.generic import CreateView
from .models import Pet, Appointment
from django.contrib.auth.mixins import LoginRequiredMixin

def index_view(request):
    return render(request, 'index.html')

class AppointmentView(LoginRequiredMixin, CreateView):
    form_class = requestAppointmentForm
    success_url = '/appointments'
    template_name = 'appointments.html'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Appointment.objects.order_by('request_date')
        return super(AppointmentView, self).get_context_data(**kwargs)
    
    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

# V This is the old function view replaced by the class view above. V
# 
# @login_required()
# def request_appointment_view(request):
#     if request.method == "POST":
#         form = requestAppointmentForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.client = User.objects.get(pk=request.user.id)
#             obj.status = 0
#             obj.save()
#             messages.success(request, "Appointment request sent successfully.")
#             return redirect('appointments')
#         else:
#             messages.error(request, "Something went wrong. Request not sent.")
#     else:
#         form = requestAppointmentForm()

#     return render(request, 'appointments.html', {'form': form})


@staff_member_required
def add_pet_view(request):
    if request.method == "POST":
        form = addPetForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.client = User.objects.get(pk=request.user.id)
            obj.status = 0
            obj.save()
            messages.success(request, "Pet added.")
            return redirect('appointments')
        else:
            messages.error(request, "Something went wrong. Request not sent.")
    else:
        form = addPetForm()

    return render(request, 'petregister.html', {'form': form})
