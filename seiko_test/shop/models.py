from django.db import models


class ProductCategory(models.Model):
    """Django model for Product categories"""

    name = models.CharField(max_length=128, null=False)  # Category's name

class Product(models.Model):
    """Django model for Products"""

    name = models.CharField(max_length=128, null=False)  # Product's name
    update_counter = models.IntegerField(default=0, null=False)  # Update in db product counter
    category_id = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT, related_name='product_category'
    )  # Product's category

class Shop(models.Model):
    """Django model for Shops"""

    name = models.CharField(max_length=128, null=False)  # Shop's name
    product_ids = models.ManyToManyField(
        Product,
    )  # Shop's product
