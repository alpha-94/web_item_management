from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login as django_login, logout as django_logout, authenticate


# Create your views here.
# CRUD Create, Update

def register(request):
    if request.method == 'POST':
        # 회원 가입 데이터 입력 완료
        user_form = RegisterForm(request.POST)
        # 올바른 회원가입 데이터 인가?
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        # 회원가입 내용을 입력하는 상황
        user_form = RegisterForm()

    return render(request, 'registration/register.html', {'form': user_form})


def login(request):
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 가져온 username과 password에 해당하는 User가 있는지 판단한다
            # 존재할경우 user변수에는 User인스턴스가 할당되며,
            # 존재하지 않으면 None이 할당된다
            user = authenticate(
                username=username,
                password=password
            )
            # 인증에 성공했을 경우
            if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)
                # Post목록 화면으로 이동
                return redirect('/')
            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,
    }

    return render(request, 'registration/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('/')
