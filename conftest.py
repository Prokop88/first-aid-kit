import pytest

from django.test import Client

from medicines.models import Medicines


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def medicines():
    return Medicines.objects.create(
        name='fake product',
        international_name='fake product description',
        dosage=2,
        expiration_date="2022-10-22",
    )