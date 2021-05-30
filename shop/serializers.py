"""
Serializer for restful api
"""
from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'stock']
