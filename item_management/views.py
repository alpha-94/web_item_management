from django.shortcuts import render

# 로그인 시 사용가능하게 만듦
# 함수 뷰 전용
from django.contrib.auth.decorators import login_required
# 클래스 뷰 전용
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import *
from entry_management.models import *
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, View
from django.views.generic.detail import DetailView
from django.shortcuts import redirect, reverse

from django_filters.views import FilterView
from django_filters.rest_framework import filters
from datetime import date
# 테이블 만들기
import django_tables2 as tables
import django_tables2.paginators as paginators
from django_tables2 import RequestConfig
import django_filters
from crispy_forms.helper import FormHelper
from .qr_code import Stream

from django.template import Context, Template
from django.http.response import StreamingHttpResponse


class Item_DetailView(DetailView):
    model = Item_info
    template_name = 'item_management/page_detail_item.html'

    def get_context_data(self, **kwargs):
        context = super(Item_DetailView, self).get_context_data(**kwargs)
        context['plus'] = Entry_Plus_Item.objects.all()
        return context


class Item_Info_Table(tables.Table):
    # select = tables.TemplateColumn('<input type= \'checkbox\' name=\'item[]\' id=\'{{record.id}}\'>', verbose_name='')
    item_code = tables.TemplateColumn('<a href=\'{% url \'item:item_detail\' pk=record.id %}\'>{{value}}</a>')

    class Meta:
        attrs = {
            "class": "table table-bordered",
            'id': 'dataTable',
            'width': '100%',
            'cellspacing': '0',
        }

        model = Item_info

        fields = ('item_code', 'item_class', 'item_name', 'item_condition')


class Item_Filter(django_filters.FilterSet):
    item_class = django_filters.ModelMultipleChoiceFilter(queryset=Item_Class.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple)


class Item_list_View(LoginRequiredMixin, tables.SingleTableMixin, FilterView):
    table_class = Item_Info_Table
    queryset = Item_info.objects.all()
    context_object_name = 'item_list'
    filterset_class = Item_Filter


# Create your views here.

def index(request):
    context = {'object': Item_info.objects.all()}
    return render(request, 'item_management/page_main.html', context)


def index_example(request):
    return render(request, 'item_management/example_cards.html')


class Item_Upload_Form(LoginRequiredMixin, forms.ModelForm):
    custom_id = forms.IntegerField(label='등록번호', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Item_info
        fields = ['id', 'group', 'item_date', 'item_class', 'item_name', 'item_price',
                  'item_condition',
                  'manager_name', 'manu_name', 'model_number', 'image']

        widgets = {
            'item_date': forms.DateInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'item_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AR + 부서 + 구매년월 + 숫자'}),
            'item_class': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'item_condition': forms.Select(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manu_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Item_UploadView(LoginRequiredMixin, CreateView):
    model = Item_info

    template_name = 'item_management/page_upload_item.html'
    form_class = Item_Upload_Form

    def form_valid(self, form):
        code_list = Item_info.objects.values('item_code')

        # print(form.instance.group)
        for codes in code_list:
            text = codes['item_code']
            # 그룹이 일치 하는지
            if text[:3] == str(form.instance.group):

                # 날짜가 일치 하는지
                if text[3:7] == form.instance.item_date.strftime('%Y%m')[-4:]:

                    # 코드가 일치 하는지
                    if text[7:11] == str(form.cleaned_data['custom_id']).zfill(4):
                        form.cleaned_data['custom_id'] += 1
                        print(form.cleaned_data['custom_id'], 'true')

            else:
                # print('false group')
                form.instance.item_code = str(form.instance.group) + form.instance.item_date.strftime('%Y%m')[-4:] + str(form.cleaned_data['custom_id']).zfill(4)
        print(form.instance.item_code)
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            # print(form.instance.item_date.strftime('%Y%m')[-4:])
            form.instance.save()
            return redirect('/item')

        else:
            return self.render_to_response({'form': form})


class Item_DeleteView(LoginRequiredMixin, DeleteView):
    model = Item_info
    success_url = '/item/'
    template_name = 'item_management/page_delete_item.html'


class Item_UpdateView(LoginRequiredMixin, UpdateView):
    model = Item_info
    success_url = '/item/'
    fields = ['item_class', 'item_name', 'item_price', 'item_condition',
              'manager_name', 'manu_name', 'model_number', 'image']

    template_name = 'item_management/page_update_item.html'


# ############################QR코드 관련############################# #
def gen():
    print('실행')
    obj = Stream()
    while True:
        frame = obj.stream()
        try:
            frame = (b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            yield frame

        except TypeError:
            obj.read_code()
            c = {'data': frame}
            print(c)
            # return c
            break


def qrcode(request):
    if request.method == 'GET':
        print('Get Video')
        # return render(request, 'item_management/qrcode_result.html', {'object': result})
        return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        print('tt')


def index_video(request):
    if request.method == 'GET':
        print('Get Index')
    return render(request, 'item_management/qrcode.html')
