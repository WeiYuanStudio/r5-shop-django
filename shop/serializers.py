"""
Serializer for restful api
"""
from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Product, Announcement


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
        fields = ['username', 'email', 'is_active', 'date_joined', 'last_login']
