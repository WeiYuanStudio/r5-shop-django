"""
View set for models
"""
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Product, Announcement
from .serializers import ProductSerializer, AnnouncementSerializer, UserSerializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.all()
    sorted = ['date']
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):  # Todo:Override other method for secure
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        """override the create func for user register"""
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            User.objects.create_user(username, email, password)
            return Response({"message": "ok"})

        except IntegrityError as e:
            if 'username' in e.__str__():
                return Response({"message": "username invalid"})

            print(e.__cause__)
            return Response({"message": "unknown error"})

        except KeyError:
            return Response({"message": "model illegal! please check your post json model"})
