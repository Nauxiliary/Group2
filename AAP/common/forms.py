from django.forms import ModelForm
from django import forms
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


class addPetForm(ModelForm):
    class Meta:
        model = Pet
        # TODO How to include / create vaccine references?
        # TODO
        #  Clients won't currently be able to add their own pets, so this foreign-key
        #  is the current best solution. However, in the future it might present issue.

        fields = ('owner', 'name', 'picture', 'breed', 'condition', 'last_seen',
                  'temperament', 'clip', 'special_instructions')

    def save(self, commit=True):
        pet = super(addPetForm, self).save(commit=False)
        if commit:
            pet.save()
        return pet
