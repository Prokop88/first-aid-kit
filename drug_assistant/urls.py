"""drug_assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.confs.urls.defaults import *
from django.contrib import admin
from django.urls import path, include
from medicines import views as ex_views
from register import views as re_views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('list_users/', ex_views.UserListView.as_view(), name='list-users'),
    path('login/', ex_views.LoginFormView.as_view(), name='login-user'),
    path('logout/', ex_views.LogoutView.as_view(), name='user-logout'),
    path('reset_password/<int:pk>', ex_views.ResetPasswordUpdate.as_view(), name='reset-password-update'),
    path('medicines_list/', ex_views.MedicinesView.as_view(), name='medicines-list'),
    path('patient_list/', ex_views.PatientView.as_view(), name='patient-list'),
    path("medicines_add/", ex_views.MedicinesAdd.as_view(), name="medicines-add"),
    path('medicines_add1/', ex_views.MedicinesAddView.as_view(), name='medicines-add1'),
    path("medicine_edit/<int:medicines_id>/", ex_views.MedicinesModify.as_view(), name="medicines-edit"),
    path("index", ex_views.index, name="index"),
    path("register1/", re_views.register, name="register1"),
    path("medicines_delete/<int:medicines_id>/", ex_views.MedicinesDelete.as_view(), name="medicines-delete"),
    path("medicine_details/<int:medicine_id>/", ex_views.MedicinesDetails.as_view(), name="medicine-details"),
    path("patient_add/", ex_views.PatientAdd.as_view(), name="Patient-add"),
]
