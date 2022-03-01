from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import requestAppointmentForm, addPetForm
from django.views.generic import CreateView
from .models import Appointment, Pet
from django.contrib.auth.mixins import LoginRequiredMixin
from .filter import PetOwnerFilter
from AAP.filter_mixin import ListFilteredMixin


def index_view(request):
    return render(request, 'index.html')


class AppointmentView(LoginRequiredMixin, CreateView):
    form_class = requestAppointmentForm
    #fields = ['request_date', 'pet']
    success_url = '/appointments'
    template_name = 'appointments.html'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Appointment.objects.order_by('request_date')
        return super(AppointmentView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


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


# class AppointmentView(LoginRequiredMixin, CreateView):
#     # https://stackoverflow.com/questions/51202612/how-to-pass-currently-logged-in-user-to-filter-py-i-e-request-based-filtering-in
#     form_class = requestAppointmentForm
#     # filter_set = PetOwnerFilter
#     model = Appointment
#
#     def dispatch(self, request, user, *args, **kwargs):
#         return super().dispatch(request, user, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         """
#         Get the context for this view.
#         """
#         kwargs['object_list'] = Appointment.objects.order_by('request_date')
#         return super(AppointmentView, self).get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         form.instance.client = self.request.user
#         return super().form_valid(form)
#
#     # def get(self, request, *args, **kwargs):
#     #     self.object_list1 = self.get_queryset()
#     #     self.object_list2 = self.get_queryset2()
#     #
#     #     context = self.get_context_data()
#     #     return self.render_to_response(context)


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
