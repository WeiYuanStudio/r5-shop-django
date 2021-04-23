from django.contrib import admin

from product.models import ProductCategory, ProductInfo

admin.site.register(ProductCategory)
admin.site.register(ProductInfo)
