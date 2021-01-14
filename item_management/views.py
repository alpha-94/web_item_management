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
from django.shortcuts import redirect, reverse

# 테이블 만들기
import django_tables2 as tables
import django_tables2.paginators as paginators
from django_tables2 import RequestConfig
import django_filters
from crispy_forms.helper import FormHelper
from .qr_code import Stream

from django.template import Context, Template
from django.http.response import StreamingHttpResponse


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


class Item_list_View(LoginRequiredMixin, tables.SingleTableView):
    table_class = Item_Info_Table
    queryset = Item_info.objects.all()
    context_object_name = 'item_list'


# Create your views here.

def index(request):
    return render(request, 'item_management/page_main.html')


def index_example(request):
    return render(request, 'item_management/example_cards.html')


class Item_Upload_Form(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Item_info
        fields = ['id', 'item_date', 'item_code', 'item_class', 'item_name', 'item_price', 'item_condition',
                  'manager_name', 'manu_name', 'model_number', 'image']

        widgets = {
            'item_date': forms.DateInput(attrs={'class': 'form-control'}),
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
        form.instance.author_id = self.request.user.id

        if form.is_valid():
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


def gen(obj):
    print('실행')
    t = Template('{{data}}')

    while True:
        frame = obj.stream()
        c = Context({'data': frame})
        try:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except TypeError:
            yield t.render(c)


def qrcode(request):
    # return render(request, 'item_management/qrcode_result.html', {'object': result})
    frame = gen(Stream())
    return StreamingHttpResponse(frame, content_type='multipart/x-mixed-replace; boundary=frame')


def index_video(request):
    return render(request, 'item_management/qrcode.html')
