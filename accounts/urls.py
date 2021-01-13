from django.urls import path
from django.contrib.auth import views as auth_view

from .views import *
# 2차 url 파일
# app_name = 'accounts' # name space

# default logged in :: http://127.0.0.1:8000/accounts/profile/
# 1. 프로필 페이지를 만든다.
# 2. 프로필 페이지가 아닌 페이지로 보내기(a. 장고 설정변경, b. 웹 서버에서 설정/redirect)


urlpatterns = [
    path('login/', login, name='login'),
    # logout의 경우 관리자 로그아웃으로 들어가는 경우가 있어서 템플릿 경로를 설정 해야함 .
    # path('logout/', logout, name='logout'),
    path('logout/', auth_view.LogoutView.as_view(template_name= 'registration/logout.html'), name='logout'),
    # 회원가입용
    path('register/', register, name='register'),
]