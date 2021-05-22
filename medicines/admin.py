from django.contrib import admin
from medicines.models import Medicines, Patients, Categorys, Medicines_Actions
# Register your models here.
admin.site.register(Medicines)
admin.site.register(Patients)
admin.site.register(Categorys)
admin.site.register(Medicines_Actions)