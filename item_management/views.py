from django.shortcuts import render

# 로그인 시 사용가능하게 만듦
# 함수 뷰 전용
from django.contrib.auth.decorators import login_required
# 클래스 뷰 전용
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return render(request, 'item_management/page_main.html')


def item_list(request):
    items = Item_info.objects.all()
    return render(request, 'item_management/page_list_item', {'objects_list': items})


class Item_UploadView(CreateView):
    model = Item_info
    fields = ['item_code', 'item_class', 'item_name', 'item_price', 'item_condition',
              'manager_name', 'manu_name', 'model_number', 'image']

    template_name = 'item_management/page_upload_item.html'

    def form_valid(self, form):
        form.instamce.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/')

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
