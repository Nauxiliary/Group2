from django.forms import ModelForm
from .models import Appointment, Pet


class requestAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["request_date"]

    def save(self, commit=True):
        appt = super(requestAppointmentForm, self).save(commit=False)
        if commit:
            appt.save()
        return appt


def addPetForm():
    class Meta:
        model = Pet
        fields = [...]

    def save(self, commit=True):
        pet = super(addPetForm, self).save(commit=False)
        if commit:
            pet.save()
        return pet
