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
    entry_code = tables.TemplateColumn('<a href=\'{% url \'entry:entry_detail\' pk=record.id %}\'>{{value}}</a></a>')

    class Meta:
        attrs = {"class": "table table-bordered"}
        model = Entry_Info
        fields = ('entry_code', 'entry_date', 'entry_name', 'entry_condition',
                  'manager_name')


class Entry_list_View(LoginRequiredMixin, tables.SingleTableView):
    table_class = Entry_Info_Table
    # table_pagination = {"per_page": 10}
    queryset = Entry_Info.objects.all()
    template_name = "entry_management/page_list_entry.html"


class Entry_Upload_Form(forms.ModelForm):
    class Meta:
        model = Entry_Info
        fields = ['entry_date', 'entry_code', 'entry_name', 'entry_condition', 'manager_name']

        widgets = {
            'entry_date': forms.DateInput(attrs={'class': 'form-control'}),
            'entry_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능합니다.'}),
            'entry_name': forms.TextInput(attrs={'class': 'form-control'}),
            'entry_condition': forms.Select(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Entry_UploadView(LoginRequiredMixin, CreateView):
    model = Entry_Info

    template_name = 'entry_management/page_upload_entry.html'
    form_class = Entry_Upload_Form

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/entry')

        else:
            return self.render_to_response({'form': form})


class Entry_DeleteView(LoginRequiredMixin, DeleteView):
    model = Entry_Info
    success_url = '/entry/'
    template_name = 'entry_management/page_delete_entry.html'


class Entry_UpdateView(LoginRequiredMixin, UpdateView):
    model = Entry_Info
    success_url = '/entry/'
    fields = ['entry_date', 'entry_name', 'entry_condition', 'manager_name']

    template_name = 'entry_management/page_update_entry.html'
