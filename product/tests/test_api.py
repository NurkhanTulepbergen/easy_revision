import pytest
from rest_framework import status
from django.urls import reverse

from product.models import Product


@pytest.mark.django_db
def test_product_list_api():
    url = reverse('product_list')  # Assuming your API is named 'product_list'

    # Arrange: create some products
    Product.objects.create(name="Smartphone", description="A smartphone", sale_price=500, quantity=100)
    Product.objects.create(name="Laptop", description="A powerful laptop", sale_price=1000, quantity=50)

    # Act: make a GET request to the API
    response = pytest.client.get(url)

    # Assert: check if the response is correct
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Ensure two products are returned
    assert response.data[0]['name'] == "Smartphone"
    assert response.data[1]['name'] == "Laptop"
