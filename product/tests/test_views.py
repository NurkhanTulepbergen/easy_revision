import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_list_view():
    # Arrange: create some products
    url = reverse('home')  # The URL of the product listing view
    response = pytest.client.get(url)

    # Assert: check if response is successful
    assert response.status_code == 200
    assert 'products' in response.context  # Make sure the 'products' context is passed
