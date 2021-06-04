"""
Serializer for restful api
"""
from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Product, Announcement, BuyerShow, ShippingAddress


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'stock']


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'date']


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'groups', 'date_joined', 'last_login']


class BuyerSerializers(serializers.ModelSerializer):
    """
    Todo:
    1. fix post customer id auto get
    2. fix unauth user post
    """

    class Meta:
        model = BuyerShow
        fields = ['id', 'title', 'customer', 'content']


class ShippingAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'customer', 'address_code', 'customer_name', 'phone']
