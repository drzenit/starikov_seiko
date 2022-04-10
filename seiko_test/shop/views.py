from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Product, Shop
from .serializers import ProductListSerializer, ProductSerializer


class ProductListView(APIView, PageNumberPagination):
    """DRF view for Products in category and shop"""

    def get(self, request, shop_id, category_id):
        """GET request for Products list"""

        products_from_shop = get_object_or_404(Shop, pk=shop_id).product_ids.all()  # Products from requested shop

        # Filter Products by category
        products_in_category_list = []
        for product in products_from_shop:
            if product.category_id.id == category_id:
                products_in_category_list.append(product)

        # Add pagination
        products = self.paginate_queryset(products_in_category_list, request, view=self)

        serializer = ProductListSerializer(products, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, shop_id, category_id):
        """POST request for add new Product in category"""

        serializer = ProductListSerializer(
            data=request.data,
            context={
                'shop_id': shop_id,
                'category_id': category_id
            },
            many=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)

class ProductView(RetrieveUpdateAPIView):
    """DRF view for one Product in category and shop"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        """Overriding method from UpdateModelMixin"""

        partial = kwargs.pop('partial', False)  # For partial update

        # Get Product and increment update counter
        instance = self.get_object()
        instance.update_counter += 1

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)
