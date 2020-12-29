from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# 아이템 품목 사항 // 사무류, 전산류, 장비류 등등 ...
class Item_class(models.Model):
    item_class = models.CharField('item_class', max_length=50, primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


# 아이템 상태 // 신규, 중고, 폐기 등등
class Item_condition(models.Model):
    item_condition = models.CharField('item_condition', max_length=50, primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


# 아이템 정보
class Item_info(models.Model):
    # user info
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    # item 기본사항
    item_code = models.CharField(max_length=50)
    item_class = models.ForeignKey(Item_class, on_delete=models.CASCADE, verbose_name='item_class')
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_condition = models.ForeignKey(Item_condition, on_delete=models.CASCADE, verbose_name='item_condition')

    # item 상세사항
    manager_name = models.CharField(max_length=50, null=True)
    manu_name = models.CharField(max_length=50, null=True) # 제조사
    model_number = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='item_image/%Y/%m/', default='item_image/no_image.png')

    # date 설정
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.username + '' + self.created.strftime('%Y-%m-%d %H:%M:%S')
