"""
View set for models
"""
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Product, Announcement, BuyerShow
from .serializers import ProductSerializer, AnnouncementSerializer, UserSerializers, BuyerSerializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.all()
    sorted = ['date']
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


class BuyerShowViewSet(viewsets.ModelViewSet):
    queryset = BuyerShow.objects.all()
    serializer_class = BuyerSerializers
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """未登录不给写权限"""
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Todo: 通过auth获得 customer id
    # def create(self, request, *args, **kwargs):
    #     post_user_id = request.user.id
    #     request.data['customer'] = post_user_id
    #     return super().create(request, *args, **kwargs)


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
                return Response({"message": "username invalid"}, 500)

            print(e.__cause__)
            return Response({"message": "unknown error"}, 500)

        except KeyError:
            return Response({"message": "model illegal! please check your post json model"}, 500)
