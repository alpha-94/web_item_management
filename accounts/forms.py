from django.contrib.auth.models import User
from django import forms


# 댓글 : dstagram_ver1
# 폼 : 폼태그 -> HTML 태그 -> 프론트 단에서 사용자의 입력을 받는 인터페이스
# 장고의 폼 : HTML 의 폼 역할, 데이터 베이스에 저장할 내용을 형식, 제약조건 결정

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords not matched!')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': '아이디'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': '비밀번호'
            }
        )
    )

