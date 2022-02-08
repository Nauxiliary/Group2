from django.forms import ModelForm
from .models import Appointment


class requestAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["request_date"]

    def save(self, commit=True):
        appt = super(requestAppointmentForm, self).save(commit=False)
        if commit:
            appt.save()
        return appt
