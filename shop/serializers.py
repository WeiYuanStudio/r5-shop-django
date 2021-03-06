"""
Serializer for restful api
"""
from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Product, Announcement, BuyerShow, ShippingAddress, Order, OrderExtend, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['show']
        depth = 1


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'datetime']


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'groups', 'date_joined', 'last_login']


class BuyerShowSerializers(serializers.ModelSerializer):
    """
    Todo:
    1. fix post customer id auto get
    2. fix unauth user post
    """

    class Meta:
        model = BuyerShow
        fields = '__all__'


class ShippingAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderExtendSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderExtend
        fields = '__all__'
        depth = 1


class ProductCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
