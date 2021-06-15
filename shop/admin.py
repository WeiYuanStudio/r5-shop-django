from django.contrib import admin
from django.contrib import messages

from shop.models import ProductCategory, Product, Order, OrderExtend, ShippingAddress, Announcement, BuyerShow


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'show', 'category')
    list_display_links = ('id', 'name')
    list_editable = ('price', 'stock', 'show')
    ordering = ['id', 'price', 'stock', 'show', 'category']
    search_fields = ('name',)
    actions = ['make_product_on_shelf', 'make_product_off_shelf']
    raw_id_fields = ('category',)

    @admin.action(description="上架产品")
    def make_product_on_shelf(self, request, queryset):
        queryset.update(show=True)
        self.message_user(request, message="上架成功", level=messages.SUCCESS)

    @admin.action(description="下架产品")
    def make_product_off_shelf(self, request, queryset):
        queryset.update(show=False)
        self.message_user(request, message="下架成功", level=messages.SUCCESS)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'submit_datetime', 'state', 'phone', 'address_detail', 'price')
    ordering = ['id', 'customer', 'submit_datetime', 'state', 'address_detail']
    list_filter = ('state',)
    search_fields = ('address',)
    actions = ['set_delivery', 'set_finished']

    @admin.action(description="配送")
    def set_delivery(self, request, queryset):
        queryset.update(state='d')
        self.message_user(request, message="接单成功", level=messages.SUCCESS)

    @admin.action(description="送达")
    def set_finished(self, request, queryset):
        queryset.update(state='f')
        self.message_user(request, message="订单完成", level=messages.SUCCESS)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'customer_name', 'phone', 'address_code', 'address_detail')


class OrderExtendAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'count', 'price')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderExtend, OrderExtendAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Announcement)
admin.site.register(BuyerShow)

# modify django default title
admin.site.site_title = "R5 SHOP"
admin.site.site_header = "R5 SHOP"
admin.site.index_title = "R5 SHOP"
