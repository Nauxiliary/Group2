from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewUserForm, UpdateUserForm

# Create your views here.
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
        # form = UpdateUserForm(request.POST)
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
