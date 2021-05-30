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


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderExtend)
admin.site.register(ShippingAddress)
admin.site.register(Product, ProductAdmin)
admin.site.register(Announcement)
admin.site.register(BuyerShow)

# modify django default title
admin.site.site_title = "R5 SHOP"
admin.site.site_header = "R5 SHOP"
admin.site.index_title = "R5 SHOP"
