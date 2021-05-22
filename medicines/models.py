import datetime
from django.db import models

# Create your models here.
MEDICINES_CHOICE_FIELD = (
    (1, "Medicines"),
    (2, "Medical component"),
    (3, "Supplement"),
    (4, "Herb"),
    (5, "Drag category N"),
    (6, "Psychotropic category P I, II, III, IV"),
    (7, "category B")
)

GENRE_CHOICE_FIELD = (
    (1, "Men"),
    (2, "Female")
)

MEDICINES_ACTION_CHOICE_FIELD = (
    (1, "Ból"),
    (2, "Przeciwzapalny"),
    (3, "Przeciwgorączkowy"),
    (4, "Nadciśnienie"),
    (5, "Cholersterol"),
    (6, "Depresja"),
    (7, "Padaczka"),
    (8, "Alzheimer"),
    (9, "Reumatyzm"),
    (10, "Uspakajające"),
    (11, "Serce"),
    (12, "Oko"),
    (13, "Antybiotyk")
)


class Medicines_Actions(models.Model):
    name = models.IntegerField(choices=MEDICINES_ACTION_CHOICE_FIELD)

    def __str__(self):
        return f"{self.name}"


class Categorys(models.Model):
    name = models.IntegerField(choices=MEDICINES_CHOICE_FIELD)

    def __str__(self):
        return f'{self.name}'


class Medicines(models.Model):
    name = models.CharField(max_length=126, unique=True)
    international_name = models.CharField(max_length=256)
    medicines_action = models.ManyToManyField(Medicines_Actions)
    dosage = models.IntegerField()
    expiration_date = models.DateField()
    category = models.ManyToManyField(Categorys)

    def __str__(self):
        return f'{self.name}'


class Patients(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    patient_age = models.DateField()
    gender = models.IntegerField(choices=GENRE_CHOICE_FIELD)

    def patient_age(self):
        return int((datetime.date.today() - self.patient_age).days / 365.25)

    def __str__(self):
        return f'{self.last_name}'


class FirstAidKits(models.Model):
    patient = models.OneToOneField(Patients, on_delete=models.CASCADE, primary_key=True)
    medicines = models.ManyToManyField(Medicines)
