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
        verbose_name_plural = verbose_name = '商品分类'

    def __str__(self):
        return self.name


class Product(models.Model):
    """for shop info"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=_PRODUCT_NAME_LEN)
    image = models.ImageField(null=True, upload_to=_IMG_UPLOAD_PATH)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    show = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = verbose_name = '商品信息'

    def __str__(self):
        return f'{self.id}: {self.name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('c', '已创建'),
        ('p', '已支付'),
        ('d', '配送中'),
        ('f', '已完成'),
    ]

    """for order"""
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)  # Todo: deleted
    submit_datetime = models.DateTimeField()
    state = models.CharField(choices=STATUS_CHOICES, max_length=1)
    address = models.CharField(max_length=_ORDER_ADDR_LEN)

    class Meta:
        verbose_name_plural = verbose_name = '订单'

    def get_state_cn_name(self, state_code):
        for state in self.STATUS_CHOICES:
            if state[0] == state_code:
                return state[1]

    def __str__(self):
        return f'{self.id}: {self.customer} {self.get_state_cn_name(self.state)} {self.submit_datetime}'


class OrderExtend(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField()
    price = models.FloatField()

    class Meta:
        verbose_name_plural = verbose_name = '扩展订单'


class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)  # Todo: deleted
    customer_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=16)
    address_code = models.CharField(max_length=12)  # use gb 2260
    address_detail = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = verbose_name = '收货地址'

    def __str__(self):
        return f'{self.id}: {self.customer} {self.customer_name} {self.address_detail}'


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    datetime = models.DateTimeField()

    class Meta:
        verbose_name_plural = verbose_name = '公告中心'

    def __str__(self):
        return f'{self.id}: {self.title}'


class BuyerShow(models.Model):
    id = models.AutoField(primary_key=True)
    publish_datetime = models.DateTimeField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)  # Todo: deleted
    title = models.CharField(max_length=256)
    content = models.TextField()

    class Meta:
        verbose_name_plural = verbose_name = '买家秀'

    def __str__(self):
        return f'{self.id}: {self.title}'
