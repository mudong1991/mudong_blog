# -*- coding:utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    """
    登录的表单form
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username', 'class': 'form-control', 'placeholder': '用户名',
                                                             'required': 'required'}),
                               max_length=50, error_messages={'required': '用户名不能为空',})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control',
                                                                 'placeholder': '密码', 'required': 'required'}),
                               max_length=30, error_messages={'required': '密码不能为空',})


class RegForm(forms.Form):
    """
    注册表单
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'user-username', 'class': 'form-control',
                                                             'placeholder': '用户名', 'required': 'required'}),
                               max_length=50, error_messages={'required': '用户名不能为空',})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'user-password', 'class': 'form-control',
                                                                 'placeholder': '密码', 'required': 'required', "autocomplete": "off"}),
                               max_length=30, error_messages={'required': '密码不能为空',})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'user-email', 'class': 'form-control',
                                                            'placeholder': '邮箱', 'required': 'required', "autocomplete": "off"}),
                             max_length=80, error_messages={'required': '邮箱不能为空'})
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'id': 'user-avatar', 'accept':
                                                            'image/png, image/gif, image/jpg, image/bmp',
                                                            'placeholder': '头像'}),
                              max_length=500, required=False)
    url = forms.URLField(widget=forms.URLInput(attrs={'id': 'user-url', 'class': 'form-control', 'placeholder': '个人网址'}),
                         max_length=100, required=False)


class CommentForm(forms.Form):
    """
    评论表单
    """
    comment = forms.CharField(widget=forms.Textarea(attrs={'id': 'comment_content', 'class': 'comment-content', 'required': 'required',
                                                           'placeholder': '说点什么吧', 'tabindex': '1'}),
                              error_messages={'required': '评论内容不能为空'})
    author = forms.CharField(widget=forms.TextInput(attrs={'id': 'comment_author', 'placeholder': '昵称','required': 'required', 'tabindex': '2'}),
                             max_length=80, error_messages={'required': '昵称不能为空',})

    email = forms.EmailField(widget=forms.TextInput(attrs={'id': 'comment_email',  'placeholder': '邮箱','required': 'required', 'tabindex': '3',
                                                           'email': True, 'invalid': 'invalid'}),
                             max_length=80, error_messages={'required': '邮箱不能为空'})

    url = forms.URLField(widget=forms.TextInput(attrs={'id': 'comment_url', 'placeholder': '网址', 'tabindex': '4'}),
                         max_length=80, required=False)

    article = forms.CharField(widget=forms.HiddenInput())
