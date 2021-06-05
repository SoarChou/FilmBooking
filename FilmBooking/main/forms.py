from django import forms
from django.forms import widgets

class user:
    username = forms.CharField( min_length=3, max_length=128, widget=forms.TextInput(attrs={
        "name":"username",
        "class":"form-control",
        "id":"id_username",
        "placeholder":"Username",
        "autofocus":"", 
        "required":""
    }))

    # <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
    password = forms.CharField( 
        # validators=[RegexValidator(r'^(?=.[0-9])(?=.[a-zA-Z])([a-zA-Z0-9]{6,20})$', '密码必须包含数字，字母', 'invalid')],
        min_length=8, 
        max_length=256, 
        widget=forms.PasswordInput(attrs={
            "name":"password",
            "class":"form-control",
            "id":"id_password",
            "placeholder":"Password",
            "required":""
        }),
    )

    email = forms.EmailField( widget=forms.EmailInput(attrs={
        "name":"email",
        "class":"form-control",
        "id":"id_email",
        "placeholder":"Email",
        "required":""
    }))

    # <input type="radio" id="customRadio1" name="customRadio" class="custom-control-input" checked>
    # <label class="custom-control-label" for="customRadio1">Oh, I'm selected!</label>
    # sex = forms.CharField( 
    #     widget=widgets.RadioSelect(choices=[(1,"女"),(2,"男"),],attrs={
    #         "name":"customRadio1",
    #         "class":"custom-control-input",
    #         "id":"customRadio1",
    #     }),
    #     initial=1,
    #     # label=

    # )
 
class UserForm(forms.Form):      
    # 用户表
    # <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required> 
    username = user.username
    password = user.password
    password_repeat = forms.CharField( max_length=256, widget=forms.PasswordInput(attrs={
        "name":"password",
        "class":"form-control",
        "id":"id_password",
        "placeholder":"RepeatPassword",
        "required":""
    }))
    email = user.email


class LoginForm(forms.Form):
    username = user.username
    password = user.password