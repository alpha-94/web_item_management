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
from django.shortcuts import redirect

from django.contrib import messages

# 테이블 만들기
import django_tables2 as tables



# Create your views here.


class Entry_DetailView(DetailView):
    model = Entry_Info
    template_name = 'entry_management/page_detail_entry.html'

    def get_context_data(self, **kwargs):
        context = super(Entry_DetailView, self).get_context_data(**kwargs)
        context['plus'] = Selected_Item_Info.objects.all()
        return context


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

    rendering = render(request, 'entry_management/test.html', {
        'items': filter_not_0_items,
        'un_items': filter_selected_items,
        'selected': selected_all,
    })

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


'''
# 자산 전체 iter
    for item in items_all:

        # item id 와 일치 하는 종합정보 필터
        selected_item = selected.filter(item_id=item.id)

        # 필터 내 들어있지 않는다면
        if not selected_item:
            selected_list_item.append(item.id)

        # 들어 있다면
        else:
            list_item.append(item.id)

    entry_id = entries.get(id=pk)

    filter_items = items_all.exclude(item_count=0)
    filter_selected_items = items_all.exclude(id__in=selected_list_item)

    if request.method == 'POST':

        for idx, i in enumerate(request.POST.getlist('item[]')):

            for se_item in selected_list_item:
                print('se_item', se_item)
                if se_item == int(i):

                    get_count = int(request.POST.getlist('count[]')[idx])
                    print('item id :: ', i, '  item_discount ::', get_count)
                    item_id = items.get(id=i)

                    item_full_count = int(item_id.item_full_count)
                    item_count = int(item_id.item_count)

                    if item_count >= get_count:
                        print('create')
                        selected.create(author_id=request.user.id,
                                        entry_id=entry_id,
                                        item_id=item_id,
                                        selected_item_count=get_count
                                        )
                        items.filter(id=i).update(item_count=item_count - get_count)

                    else:
                        print('fail')
                        return render(request, 'entry_management/test.html', {
                            'items': filter_items,
                            'un_items': filter_selected_items,
                            'selected': selected_all,
                        })

            for item in list_item:
                print('item', item)
                if item == int(i):
                    print('delete')
                    item_id = items.get(id=i)
                    selected.get(item_id=item_id).delete()

        return redirect('/entry/detail/{}'.format(pk))

    else:
        return render(request, 'entry_management/test.html', {
            'items': filter_items,
            'un_items': filter_selected_items,
            'selected': selected_all,
        })
'''
