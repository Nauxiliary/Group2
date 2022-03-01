# -*- coding: utf-8 -*-
import datetime

from django.forms import ModelForm
from django import forms
from django.http import request

from .models import Appointment, Pet, PetOwner
from django.conf import settings


class requestAppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields = ["request_date", "pet"]

    def save(self, commit=True):
        appt = super(requestAppointmentForm, self).save(commit=False)
        if commit:
            appt.save()
        return appt

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/7300076
        # self.user = kwargs.pop('user', None)
        # self.pets = Pet.objects.filter(owner=self.user)
        for key in kwargs:
            print("The key {} holds {} value".format(key, kwargs[key]))

        user = kwargs.pop('user')
        super(requestAppointmentForm, self).__init__(*args, **kwargs)

        self.fields['request_date'].queryset = Appointment.objects.filter(client=user)
        self.fields['pet'].queryset = Pet.objects.filter(owner=user)

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
