from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

ENTRY_CONDITIONS = (
    ('A', '진행'),
    ('B', '종료'),
    ('C', '예정'),
)


class Entry_Info(models.Model):
    objects = None
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='et_user', db_column='et_user')

    # entry 기본사항
    entry_code = models.CharField(max_length=100, verbose_name='사업번호')
    entry_date = models.DateField(default=datetime.today, verbose_name='사업일자')
    entry_name = models.CharField(max_length=100, verbose_name='사업명')
    entry_condition = models.CharField(max_length=100, choices=ENTRY_CONDITIONS, verbose_name='사업상태')
    manager_name = models.CharField(max_length=50, verbose_name='담당자')

    # date 설정
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.entry_code, self.entry_name)


class Selected_Item_Info(models.Model):
    item_id = models.ForeignKey('item_management.Item_Info', on_delete=models.CASCADE, related_name='se_item',
                                db_column='se_item', primary_key=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='se_user', db_column='se_user')
    entry_id = models.ForeignKey('Entry_Info', on_delete=models.CASCADE, related_name='se_entry', db_column='se_entry')

    selected_item_count = models.PositiveSmallIntegerField(verbose_name='출하량')  # 32767 자리까지
