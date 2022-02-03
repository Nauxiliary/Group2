from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import User

fields_temp = (
        'email', 'first_name', 'last_name', 'telephone', 'telephone_2',
        'street', 'city', 'state'
    )


class UserCreationForm(forms.ModelForm):
    """Form for creating new users"""
    password = forms.CharField(label='Password')
    # Asking for repeated password is bad practice.

    class Meta:
        model = User
        fields = fields_temp

    def save(self, commit=True):
        # Save password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Update users.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = fields_temp
        fields += ('is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class ClientAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = fields_temp
    list_display += ('is_admin', )

    list_filter = ('is_admin',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('telephone', 'telephone_2', 'street', 'city', 'state')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': fields_temp,
        })
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, ClientAdmin)
admin.site.unregister(Group)
