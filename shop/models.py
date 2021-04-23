import enum
from django.db import models
from django.conf import settings
from R5_SHOP.settings import STATIC_URL

# Settings of db
_PRODUCT_NAME_LEN = 128
_PRODUCT_CATEGORY_NAME_LEN = 128
_ORDER_ADDR_LEN = 1024
_IMG_UPLOAD_PATH = STATIC_URL[1:] + "img_upload"


class ProductCategory(models.Model):
    """for shop category"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=_PRODUCT_CATEGORY_NAME_LEN)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'


class ProductInfo(models.Model):
    """for shop info"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=_PRODUCT_NAME_LEN)
    image = models.ImageField(null=True, upload_to=_IMG_UPLOAD_PATH)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    show = models.BooleanField(default=True)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'


class Order(models.Model):
    class OrderStateType(enum.Enum):
        """type of order"""
        CREATED = 1
        PAYED = 2
        ON_DELIVERY = 3
        FINISHED = 4

    """for order"""
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)  # Todo: deleted
    submit_datetime = models.DateTimeField()
    state = models.IntegerField(choices=[(type.value, type) for type in OrderStateType])
    address = models.CharField(max_length=_ORDER_ADDR_LEN)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'


class OrderExtend(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField()
    price = models.FloatField()

    class Meta:
        verbose_name = '扩展订单'
        verbose_name_plural = '扩展订单'
