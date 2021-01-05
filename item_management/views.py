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


class Item_Info_Table(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Item_info
        fields = ('item_code', 'item_class', 'item_name', 'item_price', 'item_condition',
                  'manager_name', 'manu_name', 'model_number', 'image')


class Item_list_View(tables.SingleTableView):
    table_class = Item_Info_Table
    table_pagination = {"per_page": 10}
    queryset = Item_info.objects.all()
    template_name = "item_management/page_list_item.html"


# Create your views here.

def index(request):
    return render(request, 'item_management/page_main.html')


class Item_Upload_Form(forms.ModelForm):
    class Meta:
        model = Item_info
        fields = ['item_date', 'item_code', 'item_class', 'item_name', 'item_price', 'item_condition',
                  'manager_name', 'manu_name', 'model_number', 'image']

        widgets = {
            'item_date': forms.DateInput(attrs={'class': 'form-control'}),
            'item_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능합니다.'}),
            'item_class': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'item_condition': forms.Select(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manu_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),

        }


class Item_UploadView(CreateView):
    model = Item_info
    # fields = ['item_code', 'item_class', 'item_name', 'item_price', 'item_condition',
    #           'manager_name', 'manu_name', 'model_number', 'image']

    template_name = 'item_management/page_upload_item.html'
    form_class = Item_Upload_Form

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/item')

        else:
            return self.render_to_response({'form': form})


class Item_DeleteView(DeleteView):
    model = Item_info
    success_url = '/'
    template_name = 'item_management/page_delete_item.html'


class Item_UpdateView(UpdateView):
    model = Item_info
    fields = ['item_class', 'item_name', 'item_price', 'item_condition',
              'manager_name', 'manu_name', 'model_number', 'image']

    template_name = 'item_management/page_update_item.html'
