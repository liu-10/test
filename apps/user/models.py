from django.db import models
from django.contrib.auth.models import AbstractUser
from eb.base_model import BaseModel


class User(AbstractUser, BaseModel):
    """用户模块"""
    username = models.CharField(max_length=32,unique=True,verbose_name='用户名')
    email = models.CharField(max_length=256,verbose_name='邮箱')
    is_superuser = models.BooleanField(default=False,verbose_name='是否为超级用户')
    is_active = models.BooleanField(default=False,verbose_name='是否激活')
    date_joined = models.DateTimeField(null=True,verbose_name='注册时间')

    class Meta:
        db_table = 'qb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    """判断是否有默认地址"""
    def get_default_address(self, user):
        try:
            address = self.get(user=user, is_default=True)
        except Exception as e:
            address = None
        return address


class Address(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='附属用户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    address = models.CharField(max_length=256, verbose_name='收件人地址')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    is_default = models.BooleanField(default=False, verbose_name='是否为默认地址')

    # @property
    # def to_user(self):
    #     self._user, _ = User.objects.get_or_create(id=self.id)
    #     return self._user

    object = AddressManager()

    class Meta:
        db_table = 'qb_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
