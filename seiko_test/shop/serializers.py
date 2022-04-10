from rest_framework import serializers

from django.shortcuts import get_object_or_404

from .models import ProductCategory, Product, Shop


class ProductListSerializer(serializers.ModelSerializer):
    """DRF Model serializer for Products in category and shop"""

    class Meta:
        model = Product
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        """For POST method"""

        # Extract url params
        shop_id = self.context.get('shop_id')
        category_id = self.context.get('category_id')

        # Get Shop and Category needed
        shop = get_object_or_404(Shop, pk=shop_id)
        category = get_object_or_404(ProductCategory, pk=category_id)

        # Save new Product
        product = Product(name=validated_data['name'], category_id=category)
        product.save()

        # Add new product at needed shop
        shop.product_ids.add(product)

        return product

class ProductSerializer(serializers.ModelSerializer):
    """DRF Model serializer for one Product in category and shop"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'update_counter']
        read_only_fields = ['id', 'update_counter']
