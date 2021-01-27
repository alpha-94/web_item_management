from django.shortcuts import render

# 로그인 시 사용가능하게 만듦
# 함수 뷰 전용
from django.contrib.auth.decorators import login_required
# 클래스 뷰 전용
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import *

from item_management.views import *

# 예외문
from django.core.exceptions import ObjectDoesNotExist

from django import forms
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect

from django.contrib import messages

# 테이블 만들기
import django_tables2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def post_Item(request, pk):
    list_item = []  # Item_info 리스트
    selected_list_item = []  # Selected_info 리스트

    items = Item_info.objects
    entries = Entry_Info.objects
    selected = Selected_Item_Info.objects

    items_all = items.all()
    selected_all = selected.all()

    entry_id = entries.get(id=pk)

    for item in items_all:
        # item = select 항목
        selected_item = selected.filter(item_id=item.id)

        # item = select
        if selected_item:
            selected_list_item.append(item.id)

        # item =/ select
        else:
            list_item.append(item.id)

    filter_not_0_items = items_all.exclude(item_count=0)
    filter_selected_items = selected.filter(item_id__in=selected_list_item)

    filter_not_0_f = Item_Filter(request.GET, queryset=filter_not_0_items)
    filter_not_0_items = filter_not_0_f.qs

    p_n_0_i = Paginator(filter_not_0_items, 10)
    p_s_i = Paginator(filter_selected_items, 10)

    page_1 = request.GET.get('page_item', 1)
    page_2 = request.GET.get('page_se_item', 1)

    try:
        filter_not_0_items = p_n_0_i.page(page_1)
        filter_selected_items = p_s_i.page(page_2)

    except PageNotAnInteger:
        filter_not_0_items = p_n_0_i.page(1)
        filter_selected_items = p_s_i.page(1)

    except EmptyPage:
        filter_not_0_items = p_n_0_i.page(p_n_0_i.num_pages)
        filter_selected_items = p_s_i.page(p_s_i.num_pages)

    rendering = render(request, 'entry_management/test.html', {
        'items': filter_not_0_items,
        'un_items': filter_selected_items,
        'selected': selected_all,
        'entry': entry_id,
        'filter': filter_not_0_f
    })

    if request.method == 'GET':
        return rendering

    if request.method == 'POST':
        print('post start')
        for idx, i in enumerate(request.POST.getlist('item[]')):
            for f_n_0_item in filter_not_0_items:
                if f_n_0_item.id == int(i):
                    get_count = [i for i in request.POST.getlist('count[]') if i not in '']
                    get_count = int(get_count[idx])
                    item_id = items.get(id=i)

                    item_full_count = int(item_id.item_full_count)
                    item_count = int(item_id.item_count)

                    if item_count >= get_count:
                        print(item_id)
                        try:
                            print('update selected')

                            selected_count = selected.get(item_id=item_id).selected_item_count
                            selected.filter(item_id=item_id).update(selected_item_count=selected_count + get_count)
                            items.filter(id=i).update(item_count=item_count - get_count)

                        except ObjectDoesNotExist:

                            print('create selected')
                            selected.create(author_id=request.user.id,
                                            entry_id=entry_id,
                                            item_id=item_id,
                                            selected_item_count=get_count
                                            )
                            items.filter(id=i).update(item_count=item_count - get_count)

                    else:
                        print('등록할 수량을 다시 확인해 주세요')
                        messages.info(request, '등록할 수량을 다시 확인해 주세요')
                        return rendering

        for idx, i in enumerate(request.POST.getlist('selected_item[]')):
            item_id = items.get(id=i)
            item_count = int(item_id.item_count)

            selected_id = selected.get(item_id=i)

            item_full_count = int(selected_id.item_id.item_full_count)
            selected_item_count = int(selected_id.selected_item_count)

            for select in filter_selected_items:
                if select.item_id.id == int(i):
                    get_canceled_count = [i for i in request.POST.getlist('canceled_count[]') if i not in '']
                    print(get_canceled_count)
                    get_canceled_count = int(get_canceled_count[idx])

                    print(selected_item_count >= get_canceled_count)
                    print('item_count ::', selected_item_count, ',get_canceled_count ::', get_canceled_count)

                    if selected_item_count >= get_canceled_count:
                        if get_canceled_count == selected_item_count:
                            print('delete')

                            selected.get(item_id=item_id).delete()
                            items.filter(id=i).update(item_count=item_count + get_canceled_count)

                        else:
                            print('update selected')

                            selected_count = selected.get(item_id=item_id).selected_item_count
                            selected.filter(item_id=item_id).update(
                                selected_item_count=selected_count - get_canceled_count)
                            items.filter(id=i).update(item_count=item_count + get_canceled_count)

                    else:
                        print('등록할 수량을 다시 확인해 주세요')
                        messages.info(request, '등록할 수량을 다시 확인해 주세요')
                        return rendering
        return redirect('/entry/detail/{}'.format(pk))

    else:
        messages.info(request, '체크 후 수량을 적어주세요')
        return rendering


class Before_Item_Table(tables.Table):
    select = tables.TemplateColumn(
        r'<input  id="itemCheck{{item.id}}" type="checkbox" name="item[]" value="{{item.id}}" >')
    count = tables.TemplateColumn(
        r'<input style="resize:none; width:50px;" id="itemCount{{item.id}}" type="number" name="count[]" value="">')

    class Meta:
        attrs = {
            "class": "table table-bordered",
            'id': 'dataTable',
            'width': '100%',
            'cellspacing': '0',
        }

        model = Item_info

        fields = ('item_code', 'item_class', 'item_name', 'item_full_count', 'item_count')


class After_Item_Table(django_tables2.Table):
    select = tables.TemplateColumn(
        r'<input id="itemCheck{{select.item_id.id}}" class="select" type="checkbox" name="selected_item[]" value="{{select.item_id.id}}" >')
    count = tables.TemplateColumn(
        r'<input style="resize:none; width:50px;" id="itemCount{{select.item_id.id}}" type="number" name="canceled_count[]" value="">')

    class Meta:
        attrs = {
            "class": "table table-bordered",
            'id': 'dataTable',
            'width': '100%',
            'cellspacing': '0',
        }

        model = Selected_Item_Info

        fields = ('item_id.item_code', 'item_id.item_class', 'item_id.item_name', 'item_id.item_full_count',
                  'selected_item_count')


'''
class Select_View(django_tables2.MultiTableMixin, TemplateView):
    template_name = 'entry_management/test2.html'

    tables = [
        Before_Item_Table(),
        After_Item_Table(),
    ]

    table_pagination = {
        "per_page": 10
    }

    def get_context_data(self, **kwargs):
        context = super(Select_View, self).get_context_data(**kwargs)
        list_item = []  # Item_info 리스트
        selected_list_item = []  # Selected_info 리스트

        items = Item_info.objects
        entries = Entry_Info.objects
        selected = Selected_Item_Info.objects

        items_all = items.all()
        selected_all = selected.all()

        entry_id = self.kwargs['pk']

        entry_id = entries.get(id=entry_id)

        for item in items_all:
            # item = select 항목
            selected_item = selected.filter(item_id=item.id)

            # item = select
            if selected_item:
                selected_list_item.append(item.id)

            # item =/ select
            else:
                list_item.append(item.id)

        filter_not_0_items = items_all.exclude(item_count=0)
        filter_selected_items = selected.filter(entry_id=entry_id)

        b_table = Before_Item_Table(filter_not_0_items)
        a_table = After_Item_Table(filter_selected_items)

        context['table_before'] = b_table
        context['table_after'] = a_table

        return context
'''