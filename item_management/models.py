from django.db import models
from django.contrib.auth.models import User, Group, AbstractBaseUser, PermissionsMixin
from datetime import datetime
from config.settings import *


# Create your models here.

# 품목란
class Item_Class(models.Model):
    item_class = models.CharField(max_length=100, verbose_name='품목', primary_key=True)

    def __str__(self):
        return self.item_class


# 재고상태란
class Item_Condition(models.Model):
    item_condition = models.CharField(max_length=100, verbose_name='상태', primary_key=True)

    def __str__(self):
        return self.item_condition


# 아이템 정보
class Item_info(models.Model):
    # user info
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')

    # item 기본사항
    item_code = models.CharField(max_length=100, verbose_name='재고번호')
    item_date = models.DateField(default=datetime.today, verbose_name='구매일자')
    item_class = models.ForeignKey(Item_Class, on_delete=models.CASCADE, related_name='pk_class', verbose_name='품목')
    item_name = models.CharField(max_length=100, verbose_name='품명')
    item_price = models.IntegerField(verbose_name='가격')
    item_condition = models.ForeignKey(Item_Condition, on_delete=models.CASCADE, related_name='pk_condition',
                                       verbose_name='상태')

    # item 상세사항
    manager_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당자')
    manu_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='제조사')  # 제조사
    model_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='모델넘버')
    image = models.ImageField(upload_to='item_image/%Y/%m/', default='item_image/no_image.png', null=True,
                              verbose_name='사진')

    # date 설정
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.item_code, self.item_name)
