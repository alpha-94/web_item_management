from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

# 아이템 정보
class Item_info(models.Model):
    # choices data
    ITEM_CLASSES = (
        ('사무', '사무'),
        ('전산', '전산'),
        ('장비', '장비'),
    )

    ITEM_CONDITIONS = (
        ('A', '신품'),
        ('B', '중고품'),
        ('C', '대여'),
        ('D', '폐기'),
    )

    # user info
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    # item 기본사항
    item_code = models.CharField(max_length=100, verbose_name='재고번호')
    item_date = models.DateField(default=datetime.today, verbose_name='구매일자')
    item_class = models.CharField(max_length=100, choices=ITEM_CLASSES, verbose_name='품목')
    item_name = models.CharField(max_length=100, verbose_name='품명')
    item_price = models.IntegerField(verbose_name='가격')
    item_condition = models.CharField(max_length=100, choices=ITEM_CONDITIONS, verbose_name='제품상태')

    # item 상세사항
    manager_name = models.CharField(max_length=50, null=True, verbose_name='담당자')
    manu_name = models.CharField(max_length=50, null=True, verbose_name='제조사')  # 제조사
    model_number = models.CharField(max_length=50, null=True, verbose_name='모델넘버')
    image = models.ImageField(upload_to='item_image/%Y/%m/', default='item_image/no_image.png', null=True,
                              verbose_name='사진')

    # date 설정
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.item_code, self.item_name)

