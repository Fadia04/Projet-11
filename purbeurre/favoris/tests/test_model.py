"""
import pytest

from django.test import Client
from favoris.models import Favorite

@pytest.mark.django_db  
def test_favoris_model():
    client = Client()
    favoris = Favorite.objects.create(
               product = "nutella",
               user = "loulou")
    expected_value = "nutella loulou"
    assert str(favoris) == expected_value
    """