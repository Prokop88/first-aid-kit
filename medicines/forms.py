from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from .models import (
    Categorys,
    GENRE_CHOICE_FIELD,
    Medicines,
    MEDICINES_CHOICE_FIELD,
    Patients,
)

User = get_user_model()


class LoginForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = User
        fields = ["password"]

        def clean(self):
            cd = super().clean()
            username = cd["username"]
            password = cd["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error(None, "Login details incorrect")


class ResetPasswordForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["password"]

        def clean(self):
            cd = super().clean()
            if cd["password"] != cd["password2"]:
                self.add_error(None, "Passwords are different")


class MedicinesAddForm(forms.Form):
    name = forms.CharField(max_length=126)
    international_name = forms.CharField(max_length=256)
    medicines_action = forms.CharField(max_length=256)
    dosage = forms.IntegerField()
    expiration_date = forms.DateField()
    # category = forms.ChoiceField(choices=MEDICINES_CHOICE_FIELD)
    # price = forms.DecimalField(max_digits=6, decimal_places=2)
    # available = forms.BooleanField()
    # pregnant_woman_can_use = forms.BooleanField()
    # child_can_use = forms.BooleanField()


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
