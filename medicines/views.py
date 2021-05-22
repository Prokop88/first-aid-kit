from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    FormView,
    RedirectView,
    UpdateView,
)
from django.views import View
from .forms import (
    LoginForm,
    ResetPasswordForm,
    MedicinesAddForm,
    NewUserForm,
)
from .models import (
    Medicines,
    Patients,
    Categorys,
    Medicines_Actions,
    GENRE_CHOICE_FIELD,

)
from django.contrib.auth import login
from django.contrib import messages
from django.utils.dateparse import parse_date
import datetime

User = get_user_model()


# Create your views here.


class LoginFormView(FormView):
    """Login """

    model = User
    form_class = LoginForm
    template_name = "medicines/login_user.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd["username"]
        password = cd["password"]
        user = authenticate(
            username=username,
            password=password
        )
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    """logout"""
    url = reverse_lazy('login-user')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request)


class ResetPasswordUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Change password"""
    model = User
    form_class = ResetPasswordForm
    template_name = 'exercises_app/reset_password.html'
    initial = {'password': ''}
    success_url = reverse_lazy("login-user")
    permission_required = ['auth.change_user']

    def test_func(self):
        logged_user = self.request.user
        pk = self.kwargs.get(self.pk_url_kwarg)
        return logged_user.pk == pk

    def form_valid(self, form):
        self.object.set_password(form.cleand_data['password'])
        return super().form_valid(form)


class UserListView(ListView):
    """view with a list of unique users"""
    model = User
    template_name = "medicines/user_list.html"


class MedicinesView(View):
    """view with a list of all drugs"""
    template_name = "medicines/medicines_list.html"

    def get(self, request):
        medicines = Medicines.objects.all()
        medicines_actions = Medicines_Actions.objects.all()
        categorys = Categorys.objects.all()
        return render(request, self.template_name, context={"medicines": medicines,
                                                            "medicines_actions": medicines_actions,
                                                            "categorys": categorys})


class PatientView(ListView):
    """view with a list of all patients"""
    model = Patients
    template_name = "medicines/patient_list.html"


class MedicinesAdd(View):
    """view for adding drugs"""
    templates_name = "medicines/medicines_add.html"

    def get(self, request):
        categorys = Categorys.objects.all()
        medicines_actions = Medicines_Actions.objects.all()
        return render(request, self.templates_name, context={"categorys": categorys,
                                                             "medicines_actions": medicines_actions})

    def post(self, request):
        name = request.POST.get('name')
        international_name = request.POST.get('international_name')
        medicines_actions = request.POST.getlist('medicines_action')
        dosage = request.POST.get('dosage')
        expiration_date = request.POST.get('expiration_date')
        categories = request.POST.getlist('category')
        if all([name, international_name, dosage, expiration_date, categories]):
            expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
            m = Medicines.objects.create(name=name,
                                         international_name=international_name,
                                         dosage=dosage,
                                         expiration_date=expiration_date,
                                         )
            m.save()
            categories_list = Categorys.objects.filter(id__in=categories)
            medicines_actions_list = Medicines_Actions.objects.filter(id__in=medicines_actions)
            m.medicines_action.add(*medicines_actions_list)
            m.category.add(*categories_list)

            return render(request, self.templates_name, context={"message": "dodano nowy lek"})
        else:
            return render(request, self.templates_name,
                          context={'error': 'Nie uzupełniłeś wszystkich danych'})


class MedicinesAddView(View):
    """view for adding drugs"""
    templates_name = "medicines/dodawanie_leku.html"

    def get(self, request):
        form = MedicinesAddForm()
        return render(request, self.templates_name, context={'form': form})

    def post(self, request):
        form = MedicinesAddForm(request.POST)
        if form.is_valid():
            m = Medicines.objects.create(
                name=form.cleaned_data["name"],
                international_name=form.cleaned_data["international_name"],
                medicines_action=form.cleaned_data["medicines_action"],
                dosage=form.cleaned_data["dosage"],
                expiration_date=form.cleaned_data["expiration_date"],
                category=form.cleaned_data["category"],
            )
            m.save()
            categories_list = Categorys.objects.filter(id__in=categories)
            # categories_list.save()
            # medicines_actions_list = Medicines_Actions.objects.filter(id__in=medicines_actions)
            # medicines_actions_list.save()
            # m.medicines_actions.add(*medicines_actions_list)
            m.category.add(*categories_list)
            return redirect("/medicines_list/")
        return render(request, self.templates_name, context={'form': form})


class MedicinesDelete(View):
    """drug disposal view"""

    def get(self, request, medicines_id):
        medicines_to_delete = get_object_or_404(Medicines, pk=medicines_id)
        medicines_to_delete.delete()
        return redirect('/medicines_list/')


class MedicinesModify(View):
    """view for modifying drugs"""
    templates_name = "medicines/medicines_modify.html"

    def get(self, request, medicines_id):
        categorys = Categorys.objects.all()
        medicines_actions = Medicines_Actions.objects.all()
        try:
            recent_medicines = Medicines.objects.get(id=medicines_id)
        except Medicines.DoesNotExist:
            raise Http404('<h1>Page not found <h1>')
        return render(request, self.templates_name,
                      context={"categorys": categorys, 'recent_medicines': recent_medicines,
                               "medicines_actions": medicines_actions})

    def post(self, request, medicines_id):

        name = request.POST.get('name')
        international_name = request.POST.get('international_name')
        medicines_action = request.POST.get('medicines_action')
        dosage = request.POST.get('dosage')
        expiration_date = request.POST.get('expiration_date')
        categories = request.POST.getlist('category')
        m = Medicines.objects.create(name=name,
                                     international_name=international_name,
                                     dosage=dosage,
                                     expiration_date=expiration_date
                                     )
        m.save()
        categories_list = Categorys.objects.filter(id__in=categories)
        medicines_actions_list = Medicines_Actions.objects.filter(id__in=medicines_action)
        m.medicines_action.add(*medicines_actions_list)
        m.category.add(*categories_list)
        return redirect('/medicines_list/')


def index(request):
    """main page"""
    return render(request, template_name="medicines/index.html")


def add_medicines_actions_after_run():
    medicines_actions = Medicines_Actions.objects.all()
    print(medicines_actions)


class MedicinesDetails(View):
    """detail view of drugs"""

    def get(self, request, medicine_id):
        medicine = get_object_or_404(Medicines, pk=medicine_id)
        context = {
            'medicine': medicine,
        }
        return render(request, 'medicines/medicine_details.html', context)


class PatientAdd(View):
    templates_name = "medicines/patient_add.html"

    def get(self, request):
        return render(request, self.templates_name)

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        patient_age = request.POST.get("patient_age")
        gender = request.POST.get("gender")
        if all([first_name, last_name, patient_age]):
            patient_age = datetime.datetime.strptime(patient_age, "%Y-%m-%d").date()
            Patients.objects.create(
                first_name=first_name,
                last_name=last_name,
                patient_age=patient_age,
            )
            return render(request, self.templates_name, context={"message": "dodano Pacjenta"})
        else:
            return render(request, self.templates_name,
                          context={'error': 'Nie uzupełniłeś wszystkich danych'})