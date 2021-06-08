"""
View set for models
"""
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Product, Announcement, BuyerShow, ShippingAddress
from .serializers import ProductSerializer, AnnouncementSerializer, UserSerializers, BuyerShowSerializers, \
    ShippingAddressSerializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.all()
    sorted = ['date']
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.AllowAny]


class BuyerShowViewSet(viewsets.ModelViewSet):
    queryset = BuyerShow.objects.all()
    serializer_class = BuyerShowSerializers
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """未登录不给写权限"""
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            r = request.data
            BuyerShow.objects.create(publish_datetime=datetime.now(),
                                     customer=request.user,
                                     title=r['title'],
                                     content=r['content'])
            return Response({"message": "ok"})

        except KeyError as e:
            return Response({"message": "json obj error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                return Response({"message": "username invalid"}, status.HTTP_400_BAD_REQUEST)

            print(e.__cause__)
            return Response({"message": "unknown error"}, status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"message": "model illegal! please check your post json model"},
                            status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_self_user_info(self, request):
        """get user self info"""
        """return user self info"""
        user = User.objects.filter(id=request.user.id).first()
        require_key = ['id', 'username', 'email', 'is_staff', 'date_joined', 'is_superuser']
        user_info = {key: user.__dict__[key] for key in require_key}
        return Response(user_info)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializers
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            r = request.data
            ShippingAddress.objects.create(customer=self.request.user,
                                           customer_name=r['customer_name'],
                                           phone=r['phone'],
                                           address_code=r['address_code'],
                                           address_detail=r['address_detail'])

            return Response({"message": "ok"})

        except IntegrityError as e:
            if 'username' in e.__str__():
                return Response({"message": "username invalid"}, status.HTTP_400_BAD_REQUEST)

            print(e.__cause__)
            return Response({"message": "unknown error"}, status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"message": "model illegal! please check your post json model"},
                            status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.action == 'list':
            return ShippingAddress.objects.filter(customer=self.request.user.id)  # only return self addr
        return super().get_queryset()
