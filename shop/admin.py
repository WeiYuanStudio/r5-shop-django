from django.contrib import admin

from shop.models import ProductCategory, ProductInfo, Order, OrderExtend

admin.site.register(ProductCategory)
admin.site.register(ProductInfo)
admin.site.register(Order)
admin.site.register(OrderExtend)
