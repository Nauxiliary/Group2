"""AAP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common import views
from common.views import AppointmentView

urlpatterns = [
    path('admin/',              admin.site.urls),
    path('',                    views.index_view, name="mainhome"),
    path(r'^appointments/$', AppointmentView.as_view(
        template_name='appointments.html', success_url='/appointments'),
         name='appointments'),
    path('petregister/', views.add_pet_view, name="petregister"),

    path('accounts/', include('accounts.urls')),
]
