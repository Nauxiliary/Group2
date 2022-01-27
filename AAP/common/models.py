from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class Person(BaseModel):
#
#     first_name = models.CharField(max_length=35)
#     last_name = models.CharField(max_length=35)
#
#     street_address = models.CharField(max_length=35)
#     town = models.CharField(max_length=20)
#     state = models.CharField(max_length=15)
#     postal = models.CharField(max_length=9)
#
#     email = models.CharField(max_length=254)
#     phone = models.CharField(max_length=15)
#
#     username = models.CharField(max_length=70)
#     password = models.CharField(max_length=255)
#     # TODO Do we want to store passwords?
#
#     class Meta:
#         abstract = True


class Vaccine(BaseModel):
    administered_by = models.ManyToManyField('accounts.Reference', through="VaccineReference")
    local_name = models.CharField(max_length=100)
    date_administered = models.DateField("date pet was administered vaccine")


class VaccineReference(models.Model):
    # Cannot delete reference if administered vaccine.
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT)
    # Delete all vaccines if reference is deleted.
    reference = models.ForeignKey('accounts.Reference', on_delete=models.CASCADE)


class Pet(BaseModel):
    # Cannot delete vaccine if tied to pet.
    vaccine = models.ManyToManyField(Vaccine, through="PetVaccine")

    breed = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    special_instructions = models.CharField(max_length=255)
    last_seen = models.DateTimeField('pet last seen')
    picture = models.BinaryField()
    temperament = models.CharField(max_length=1)
    clip = models.CharField(max_length=255)


class PetVaccine(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT)


class Form(BaseModel):
    # When deleting the client, do not delete all forms.
    # Forms must first be dealt with before deleting the client.
    client = models.ForeignKey('accounts.Client', on_delete=models.PROTECT)

    pet = models.ManyToManyField(Pet, blank=False, through="PetForm")

    printed = models.BooleanField()


class PetForm(models.Model):
    # If a pet is deleted, delete all related forms.
    # That being said, these forms will likely already have been printed.
    # They just cannot be printed again.
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.PROTECT)


class Schedule(BaseModel):
    employee = models.ManyToManyField('accounts.Employee', through="ScheduleEmployee")
    pet = models.ManyToManyField(Pet, through="SchedulePet")


class ScheduleEmployee(models.Model):
    # When deleting the schedule, do not delete associated employee.
    # Employee must first be dealt with before deleting the schedule.
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    employee = models.ForeignKey('accounts.Employee', on_delete=models.PROTECT)

    relation = models.CharField(max_length=1)


class SchedulePet(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    # When a pet is deleted, delete all schedules with said pet.
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


class Appointment(BaseModel):
    # When client is deleted, all related appointments are also deleted.
    client = models.ForeignKey('accounts.Client', on_delete=models.CASCADE)

    request_date = models.DateTimeField("date and time client requested")
    status = models.CharField(max_length=1)
