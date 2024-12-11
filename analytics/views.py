from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product


@api_view(['GET'])
def product_trends(request):
    # Aggregate product sales by category
    trends = Product.objects.values('category__name').annotate(total_sold=Sum('quantity_sold'))
    data = {
        "categories": [trend['category__name'] for trend in trends],
        "sales": [trend['total_sold'] for trend in trends]
    }
    return Response(data)
