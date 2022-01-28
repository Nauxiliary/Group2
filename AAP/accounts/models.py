"""
scopyleft.
“Advanced Django User Model Inheritance | Blog | Scopyleft,”
May 8, 2013.
http://scopyleft.fr/blog/2013/django-model-advanced-user-inheritance/.
https://gist.github.com/vinyll/6103202
"""


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager as DjBaseUserManager)

from model_utils.managers import InheritanceManager


class BaseUserManager(DjBaseUserManager, InheritanceManager):
    """
    Manager for all Users types
    create_user() and create_superuser() must be overriden as we do not use
    unique username but unique email.
    """

    def create_user(self, email=None, password=None, **extra_fields):
        now = timezone.now()
        email = BaseUserManager.normalize_email(email)
        u = GenericUser(email=email, is_superuser=False, last_login=now,
                        **extra_fields)
        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_superuser = True
        u.save(using=self._db)
        return u


class CallableUser(AbstractBaseUser):
    """
    The CallableUser class allows to get any type of user by calling
    CallableUser.objects.get_subclass(email="my@email.dom") or
    CallableUser.objects.filter(email__endswith="@email.dom").select_subclasses()
    """
    objects = BaseUserManager()


class AbstractUser(CallableUser):
    """
    Here are the fields that are shared among specific User subtypes.
    Making it abstract makes 1 email possible in each User subtype.
    """
    email = models.EmailField(unique=True)
    is_superuser = False
    objects = BaseUserManager()

    def __unicode__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = USERNAME_FIELD

    class Meta:
        abstract = True


class GenericUser(AbstractUser):
    """
    A GenericUser is any type of system user (such as an admin).
    This is the one that should be referenced in settings.AUTH_USER_MODEL
    """
    is_superuser = models.BooleanField(default=False)


class Professional(AbstractUser):
    """
    User subtype with specific fields and properties
    """
    company = models.CharField(max_length=50)


class Individual(AbstractUser):
    """
    User subtype with specific fields and properties
    """
    name = models.CharField(max_length=50)


class Employee(AbstractUser):
    wage = models.DecimalField(decimal_places=2, max_digits=16)
    salary = models.DecimalField(decimal_places=2, max_digits=16)
    trained = models.DateField('trained on')


class Reference(AbstractUser):
    type = models.CharField(max_length=1)
    last_seen = models.DateField('last seen')
    relationship = models.CharField(max_length=50)


class Client(AbstractUser):
    reference = models.ManyToManyField(Reference, through="ClientReference")
    status = models.CharField(max_length=1)
    how_heard_about = models.CharField(max_length=255)


class ClientReference(models.Model):
    # TODO Rethink
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    # Cannot delete a reference if tied to a client.
    reference = models.ForeignKey(Reference, on_delete=models.PROTECT)


