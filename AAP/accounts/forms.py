import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

# Create your forms here.

class NewUserForm(UserCreationForm):
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
