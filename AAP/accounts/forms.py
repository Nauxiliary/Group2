import email
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import User


STATES = (
    ('', 'Choose...'),
    ('CO', 'Colorado'),
    ('AZ', 'Arizona'),
    ('NY', 'New York')
)




class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    street = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.ChoiceField(choices=STATES)
    telephone = forms.CharField(required=True, max_length=12)
    telephone_2 = forms.CharField(required=False, max_length=12)

    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2", "first_name", "last_name", "street", 
                  "city", "state", "telephone", "telephone_2"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewStaffMemberForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields=("email","password1","password2")

    def save(self, commit=True):
        user = super(NewStaffMemberForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    telephone_2 = forms.CharField(required=False)
    email = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    street = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.ChoiceField(choices=STATES)
    telephone = forms.CharField(required=True, max_length=12)
    telephone_2 = forms.CharField(required=False, max_length=12)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "street", 
                  "city", "state", "telephone", "telephone_2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True 
       
    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
