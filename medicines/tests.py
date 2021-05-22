import pytest
from medicines.models import Medicines


# Create your tests here.
def test_example():
    assert 1 == 1


@pytest.mark.django_db
def test_display_medicines_detail_site(medicines, client):
    pk = medicines.pk
    response = client.get(f'/medicine_details/{pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_medicines(client):
    response = client.get(f'/medicines_list/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_medicines(client):
    response = client.post('/medicines_add/',
                           {'name': 'Nebilet',
                            'international_name': 'nebivolol',
                            'medicines_action': 1,
                            'dosage': 1,
                            "expiration_date": "2022-10-11",
                            "category": 1

                            })
    assert Medicines.objects.get(name='Nebilet')
    assert response.status_code == 200
