from django.shortcuts import render

# 로그인 시 사용가능하게 만듦
# 함수 뷰 전용
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# 클래스 뷰 전용
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import *
from entry_management.models import *

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect, reverse

from django_filters.views import FilterView

# 테이블 만들기
import django_tables2 as tables

import django_filters

from .qr_code import Stream

from django.http.response import StreamingHttpResponse


class Item_DetailView(DetailView):
    model = Item_info
    template_name = 'item_management/page_detail_item.html'

    def get_context_data(self, **kwargs):
        context = super(Item_DetailView, self).get_context_data(**kwargs)
        context['plus'] = Selected_Item_Info.objects.all()
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

    item_name = django_filters.CharFilter(field_name='item_name',
                                          lookup_expr='icontains',
                                          label='품명')


class Item_list_View(LoginRequiredMixin, tables.SingleTableMixin, FilterView):
    table_class = Item_Info_Table
    queryset = Item_info.objects.all()
    context_object_name = 'item_list'
    filterset_class = Item_Filter


# Create your views here.

def index(request):
    date_keys = ['y_2020_m_{}'.format(i) for i in range(1, 13)]
    date_values = [Item_info.objects.filter(item_date__year='2020', item_date__month=i) for i in range(1, 13)]
    date_dic = dict(zip(date_keys, date_values))

    context = {
        'object': Item_info.objects.all(),
        'sort_date_object': Item_info.objects.all().order_by('item_date'),
        'add_all_price':Item_info.objects.only('item_price').aggregate(Sum('item_price')),

        # 품목별 현황
        'office': Item_info.objects.filter(item_class='사무'),
        'equipment': Item_info.objects.filter(item_class='장비'),
        'computational': Item_info.objects.filter(item_class='전산'),
        'part': Item_info.objects.filter(item_class='부품'),
        'tool': Item_info.objects.filter(item_class='수공구'),

        'office_price': Item_info.objects.filter(item_class='사무').aggregate(Sum('item_price')),
        'equipment_price': Item_info.objects.filter(item_class='장비').aggregate(Sum('item_price')),
        'computational_price': Item_info.objects.filter(item_class='전산').aggregate(Sum('item_price')),
        'part_price': Item_info.objects.filter(item_class='부품').aggregate(Sum('item_price')),
        'tool_price': Item_info.objects.filter(item_class='수공구').aggregate(Sum('item_price')),

        # 부서별 현황
        'ARM': Item_info.objects.filter(group=1),
        'ARP': Item_info.objects.filter(group=2),
        'ARF': Item_info.objects.filter(group=3),

        # 월별 현황
        'y_2020': Item_info.objects.filter(item_date__year='2020')
    }
    context.update(date_dic)
    return render(request, 'item_management/page_main.html', context)


def index_analyze(request):
    date_keys = ['y_2020_m_{}'.format(i) for i in range(1, 13)]
    date_values = [Item_info.objects.filter(item_date__year='2020', item_date__month=i) for i in range(1, 13)]
    date_dic = dict(zip(date_keys, date_values))

    context = {
        'object': Item_info.objects.all(),

        # 품목별 현황
        'office': Item_info.objects.filter(item_class='사무'),
        'equipment': Item_info.objects.filter(item_class='장비'),
        'computational': Item_info.objects.filter(item_class='전산'),
        'part': Item_info.objects.filter(item_class='부품'),
        'tool': Item_info.objects.filter(item_class='수공구'),

        'office_price': Item_info.objects.filter(item_class='사무').aggregate(Sum('item_price')),
        'equipment_price': Item_info.objects.filter(item_class='장비').aggregate(Sum('item_price')),
        'computational_price': Item_info.objects.filter(item_class='전산').aggregate(Sum('item_price')),
        'part_price': Item_info.objects.filter(item_class='부품').aggregate(Sum('item_price')),
        'tool_price': Item_info.objects.filter(item_class='수공구').aggregate(Sum('item_price')),

        # 부서별 현황
        'ARM': Item_info.objects.filter(group=1),
        'ARP': Item_info.objects.filter(group=2),
        'ARF': Item_info.objects.filter(group=3),

        # 월별 현황
        'y_2020': Item_info.objects.filter(item_date__year='2020')
    }
    context.update(date_dic)
    return render(request, 'item_management/page_analyze.html', context)


class Item_Upload_Form(LoginRequiredMixin, forms.ModelForm):
    custom_id = forms.IntegerField(label='등록번호', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Item_info
        fields = ['id', 'group', 'item_date', 'item_class', 'item_name', 'item_price',
                  'item_full_count', 'item_condition',
                  'manager_name', 'manu_name', 'model_number', 'image']

        widgets = {
            'item_date': forms.DateInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'item_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AR + 부서 + 구매년월 + 숫자'}),
            'item_class': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'item_full_count': forms.NumberInput(attrs={'class': 'form-control'}),
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

        # 재고번호 규격화 > 재고번호가 겹칠 경우 대비 최근에 있었던 재고번호에 +1 증가시켜 재고번호 부여
        for codes in code_list:
            text = codes['item_code']
            # 그룹이 일치 하는지
            if text[:3] == str(form.instance.group):

                # 날짜가 일치 하는지
                if text[3:7] == form.instance.item_date.strftime('%Y%m')[-4:]:

                    # 코드가 일치 하는지
                    if text[7:11] == str(form.cleaned_data['custom_id']).zfill(4):
                        form.cleaned_data['custom_id'] += 1
                        # print(form.cleaned_data['custom_id'], 'true')
            else:
                pass

        form.instance.item_code = str(form.instance.group) \
                                  + form.instance.item_date.strftime('%Y%m')[-4:] \
                                  + str(form.cleaned_data['custom_id']).zfill(4)
        print(form.instance.item_code)
        form.instance.author_id = self.request.user.id
        form.instance.item_count = form.instance.item_full_count

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
