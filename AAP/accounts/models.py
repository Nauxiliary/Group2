from django.contrib.auth.models import (AbstractUser, PermissionsMixin, BaseUserManager)
from django.db import models
from django.utils import timezone


class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """

    def create_user(self, email, name, password=None):
        """ Create a new client profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        client = self.model(email=email, password=password)

        client.set_password(password)
        client.save(using=self.db)
        client.is_staff = False

        return client

    def create_superuser(self, email, password):
        """ Create a new superuser profile """
        user = self.create_user(email, password)
        # user.is_superuser = True
        # user.is_staff = True
        user.is_admin = True
        user.is_staff = True

        user.save(using=self.db)

        return user


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    telephone = models.CharField(max_length=15)
    telephone_2 = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=2)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField('Date Joined', default=timezone.now)

    objects = UserProfileManager()

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta(object):
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """ RETURN STRING REP. OF USER EMAIL"""
        return self.email

    def has_perm(self, perm, obj=None):
        """ Does the user have a specific permission? """
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        print(self.is_admin)
        return self.is_admin
