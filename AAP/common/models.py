from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(BaseModel):

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)

    street_address = models.CharField(max_length=35)
    town = models.CharField(max_length=20)
    state = models.CharField(max_length=15)
    postal = models.CharField(max_length=9)

    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)

    username = models.CharField(max_length=70)
    password = models.CharField(max_length=255)
    # TODO Do we want to store passwords?

    class Meta:
        abstract = True


class Employee(Person):
    wage = models.DecimalField(decimal_places=2, max_digits=16)
    salary = models.DecimalField(decimal_places=2, max_digits=16)
    trained = models.DateField('trained on')


class Client(Person):
    status = models.CharField(max_length=1)
    how_heard_about = models.CharField(max_length=255)


class Reference(Person):
    type = models.CharField(max_length=1)
    last_seen = models.DateField('last seen')
    relationship = models.CharField(max_length=50)

