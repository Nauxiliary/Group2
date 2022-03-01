# -*- coding: utf-8 -*-

import datetime
import sys

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BasePerson(BaseModel):
    email = models.EmailField(max_length=254, unique=True)
    telephone = models.CharField(max_length=15)
    telephone_2 = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=2)


class Reference(BasePerson):
    type = models.CharField(max_length=1)
    relationship = models.CharField(max_length=50)


class Vaccine(BaseModel):
    administered_by = models.ManyToManyField(
        Reference, through="VaccineReference")
    local_name = models.CharField(max_length=100)
    date_administered = models.DateField("date pet was administered vaccine")


class VaccineReference(models.Model):
    # Cannot delete reference if administered vaccine.
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT)
    # Delete all vaccines if reference is deleted.
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)


class Pet(BaseModel):
    # Cannot delete vaccine if tied to pet.
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through="PetOwner", related_name="owner")
    vaccine = models.ManyToManyField(Vaccine, through="PetVaccine", related_name="vaccine")

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=255)
    condition = models.CharField(max_length=255, blank=True)
    special_instructions = models.CharField(max_length=255, blank=True)
    last_seen = models.DateTimeField('pet last seen', blank=True, default=now)
    picture = models.ImageField(upload_to='petimages/', blank=True)
    temperament = models.CharField(max_length=1, blank=True)
    clip = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        pretty = self.name
        if self.breed != "":
            pretty += "(%s)" % self.breed
        return pretty


class PetVaccine(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)


class PetOwner(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Form(BaseModel):
    # When deleting the client, do not delete all forms.
    # Forms must first be dealt with before deleting the client.
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    pet = models.ManyToManyField(Pet, blank=False, through="PetForm")

    printed = models.BooleanField()


class PetForm(models.Model):
    # If a pet is deleted, delete all related forms.
    # That being said, these forms will likely already have been printed.
    # They just cannot be printed again.
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.PROTECT)


# class Schedule(BaseModel):
#     employee = models.ManyToManyField(Employee, through="ScheduleEmployee")
#     pet = models.ManyToManyField(Pet, through="SchedulePet")
#
#
# class ScheduleEmployee(models.Model):
#     # When deleting the schedule, do not delete associated employee.
#     # Employee must first be dealt with before deleting the schedule.
#     schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
#     employee = models.ForeignKey('accounts.Employee', on_delete=models.PROTECT)
#
#     relation = models.CharField(max_length=1)


# class SchedulePet(models.Model):
#     schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
#     # When a pet is deleted, delete all schedules with said pet.
#     pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


class Appointment(BaseModel):
    # When client is deleted, all related appointments are also deleted.
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)

    request_date = models.DateTimeField("date and time client requested")
    status = models.CharField(max_length=1)

    class Meta:
        ordering = ["-request_date", "pet"]
