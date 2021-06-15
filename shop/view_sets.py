"""
View set for models
"""
from datetime import datetime

from django.db import IntegrityError, transaction
from django.db.models import F
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Product, Announcement, BuyerShow, ShippingAddress, Order, OrderExtend, ProductCategory
from .serializers import ProductSerializer, AnnouncementSerializer, UserSerializers, BuyerShowSerializers, \
    ShippingAddressSerializers, OrderSerializers, OrderExtendSerializers, ProductCategorySerializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(show=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.order_by('-datetime')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.AllowAny]


class BuyerShowViewSet(viewsets.ModelViewSet):
    queryset = BuyerShow.objects.order_by('-publish_datetime')
    serializer_class = BuyerShowSerializers
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']

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
        """return user self info"""
        if request.user.id is None:
            return Response({"message": "please login"})

        user = User.objects.filter(id=request.user.id).first()
        require_key = ['id', 'username', 'email', 'is_staff', 'date_joined']
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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print(request.data)

        try:
            with transaction.atomic():
                address = request.data.get('addressInfo')
                cart = request.data.get('cartInfo')

                order = Order.objects.create(customer=self.request.user,
                                             submit_datetime=datetime.now(),
                                             state='p',
                                             customer_name=address['name'],
                                             phone=address['tel'],
                                             address_code='',
                                             address_detail=address['address'],
                                             price=0)

                order_sum = 0

                for cart_id, cart_num in cart.items():
                    if cart_num != 0:
                        # 减库存
                        product = Product.objects.get(id=cart_id)
                        product.stock = F('stock') - cart_num
                        product.save()
                        # 检查库存
                        if Product.objects.get(id=cart_id).stock < 0:
                            raise RuntimeError('库存不足，下单失败')
                        # 计算子订单需要的信息[单件总价]
                        product = Product.objects.get(id=cart_id)
                        each_product_sum = product.price * cart_num
                        # 增加子订单
                        OrderExtend.objects.create(order=order,
                                                   product=product,
                                                   count=cart_num,
                                                   price=each_product_sum)

                        order_sum += each_product_sum

                # 写入总金额
                order.price = order_sum
                order.save()

        except RuntimeError as e:
            return Response({"message": e.__str__()}, status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OK"})

    def get_queryset(self):
        if self.action == 'list':
            return Order.objects.filter(customer=self.request.user.id).order_by('-id')  # only return self addr
        return super().get_queryset()


class OrderExtendViewSet(viewsets.ModelViewSet):
    queryset = OrderExtend.objects.all()
    serializer_class = OrderExtendSerializers
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializers
    permission_classes = [permissions.AllowAny]
