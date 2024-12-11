import pytest

from product.models import Category, Product


@pytest.mark.django_db
def test_product_creation():
    # Arrange: create a category
    category = Category.objects.create(name="Electronics")

    # Act: create a product
    product = Product.objects.create(
        name="Smartphone",
        description="A smartphone with 128GB storage",
        sale_price=500,
        quantity=100,
        category=category
    )

    # Assert: check if the product is created
    assert product.name == "Smartphone"
    assert product.category.name == "Electronics"
    assert product.sale_price == 500
    assert product.quantity == 100
    assert product.description == "A smartphone with 128GB storage"
