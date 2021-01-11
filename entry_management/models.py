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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_entry')

    # entry 기본사항
    entry_code = models.CharField(max_length=100, verbose_name='사업번호')
    entry_date = models.DateField(default=datetime.today, verbose_name='사업일자')
    entry_name = models.CharField(max_length=100, verbose_name='사업명')
    entry_condition = models.CharField(max_length=100, choices=ENTRY_CONDITIONS, verbose_name='사업상태')
    manager_name = models.CharField(max_length=50, verbose_name='담당자')

    # date 설정
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
