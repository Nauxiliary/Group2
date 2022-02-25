from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewUserForm, UpdateUserForm, PasswordChangeForm


@login_required()
def index_view(request):
    return render(request, 'index.html')


@login_required()
def dashboard_view(request):
    return render(request, 'dashboard.html')


def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('login_url')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required()
def profile_view(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was updated successfully')
            return redirect(to='profile')
        else:
            messages.error(request, "Something went wrong. Account not updated.")
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'profile.html', {'form': user_form})

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Call update_session_auth_hash() after you save the form.
            # Otherwise the user’s auth session will be invalidated and
            # she/he will have to log in again.
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password.html', {'form': form})
