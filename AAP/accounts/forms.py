import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User


STATES = (
    ('', 'Choose...'),
    ('CO', 'Colorado'),
    ('AZ', 'Arizona'),
    ('NY', 'New York')
)




class NewUserForm(UserCreationForm):
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    
    email = forms.EmailField(required=True)

    class Meta:
        # model = User
        model = get_user_model()
        fields = ("email", "password1", "password2")
        # fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    street = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.ChoiceField(choices=STATES)
    phone_number = forms.CharField(max_length=12)
    


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

    # TODO - How do we change the password?
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
