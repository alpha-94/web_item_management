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


app_name = 'entry'

urlpatterns = [
    path('', Entry_list_View.as_view(), name='entry_list'),
    path('detail/<int:pk>', DetailView.as_view(model=Entry_Info, template_name='entry_management/page_detail_entry.html'),
         name='entry_detail'),
    path('upload/', Entry_UploadView.as_view(), name='entry_upload'),
    path('delete/<int:pk>', Entry_DeleteView.as_view(), name='entry_delete'),
    path('update/<int:pk>', Entry_UpdateView.as_view(), name='entry_update'),  # <int:pk>
    path('test/<int:pk>', Item_list_View_by_Entry.as_view(template_name='entry_management/test.html'), name='test'),
]


# Item_list_View_by_Entry.as_view(template_name='entry_management/test.html')
