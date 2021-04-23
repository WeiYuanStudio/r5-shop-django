from django.db import models
from R5_SHOP.settings import STATIC_URL

# Settings of db
_PRODUCT_NAME_LEN = 128
_PRODUCT_CATEGORY_NAME_LEN = 128
_IMG_UPLOAD_PATH = STATIC_URL[1:] + "img_upload"


class ProductCategory(models.Model):
    """for product category"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=_PRODUCT_CATEGORY_NAME_LEN)


class ProductInfo(models.Model):
    """for product info"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=_PRODUCT_NAME_LEN)
    image = models.ImageField(null=True, upload_to=_IMG_UPLOAD_PATH)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
