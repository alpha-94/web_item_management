from django.shortcuts import render

# 로그인 시 사용가능하게 만듦
# 함수 뷰 전용
from django.contrib.auth.decorators import login_required
# 클래스 뷰 전용
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import *
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect

# 테이블 만들기
import django_tables2 as tables
import django_tables2.paginators as paginators
from django_tables2 import RequestConfig
import django_filters
from crispy_forms.helper import FormHelper


# Create your views here.

class Entry_Info_Table(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Entry_Info
        fields = ('entry_code', 'entry_date', 'entry_name', 'entry_condition',
                  'manager_name')


class Entry_list_View(tables.SingleTableView):
    table_class = Entry_Info_Table
    table_pagination = {"per_page": 10}
    queryset = Entry_Info.objects.all()
    template_name = "entry_management/page_list_entry.html"
