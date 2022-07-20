from django import forms
from django.forms import widgets
from Automation.models import *
from django.core.exceptions import ValidationError
class user_form(forms.Form):
    name = forms.CharField(max_length=32, label="名字", error_messages={"required": "该字段不能为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(max_length=32, label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages={"required": "该字段不能为空"})

    r_pwd = forms.CharField(max_length=32, label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                            error_messages={"required": "该字段不能为空"})
    email = forms.EmailField(label="邮箱", error_messages={"required": "该字段不能为空", "invalid": "格式不正确"},
                             widget=widgets.TextInput(attrs={"class": "form-control"}))
    tel = forms.CharField(max_length=11, label="电话", error_messages={"required": "该字段不能为空", "invalid": "格式不正确"},
                          widget=widgets.TextInput(attrs={"class": "form-control"}))
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_obj = UserAuto.objects.filter(username=name).first()
        if user_obj:
            raise ValidationError("该用户已注册")

        else:
            return self.cleaned_data.get('name')
    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        user_obj = UserAuto.objects.filter(telephone=tel).first()
        if user_obj:
            raise ValidationError("已存在改手机号")

        else:
            return self.cleaned_data.get('tel')
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        r_pwd = self.cleaned_data.get('r_pwd')
        if pwd==r_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致")

class function_form(forms.Form):
    name = forms.CharField(max_length=12, label="功能中文名称（不超过12个字符）", error_messages={"required": "该字段不能为空","invalid":"格式不正确"},
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    eng_name = forms.CharField(max_length=10, label="功能英文名称（不超过10个字符）", widget=widgets.TextInput(attrs={"class": "form-control"}),
                          error_messages={"required": "该字段不能为空","invalid":"格式不正确"})


class case_form(forms.Form):
    name = forms.CharField(max_length=12, label="用例名称（不超过12个字符）", error_messages={"required": "该字段不能为空","invalid":"格式不正确"},
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    desc = forms.CharField(max_length=64, label="用例描述（不超过64个字符）", error_messages={"required": "该字段不能为空","invalid":"格式不正确"},
                           widget=widgets.Textarea(attrs={"class": "form-control","style":"height:40px"}))

