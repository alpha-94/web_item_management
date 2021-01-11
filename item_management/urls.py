"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.detail import DetailView
from .views import *

app_name = 'item'

urlpatterns = [
    path('', Item_list_View.as_view(), name='item_list'),
    path('example/', index_example, name='example'),
    path('detail/<int:pk>', DetailView.as_view(model=Item_info, template_name='item_management/page_detail_item.html'),
         name='item_detail'),
    path('upload/', Item_UploadView.as_view(), name='item_upload'),
    path('delete/<int:pk>', Item_DeleteView.as_view(), name='item_delete'),
    path('update/<int:pk>', Item_UpdateView.as_view(), name='item_update'),  # <int:pk>
    path('qrcode/', qrcode, name='qrcode'),
    path('qrcode_result/', qrcode, name='qrcode'),
]
