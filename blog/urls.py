# -*-coding:utf-8 -*-
from django.conf.urls import url
from blog.views import *

urlpatterns = [
    # 首页
    url(r'^$', index, name='index'),
    # 分类导航页
    url(r'^category/(?P<category_name>\w+)/$', category, name='category'),
    # 标签页
    url(r'^tag/(?P<tag_name>\w+)/$', tag, name='tag'),
    # 文章详情页
    url(r'^article/$', article, name='article'),
    # 搜索文章
    url(r'^search/$', search, name='search'),
    # 评论提交表单
    url(r'^comment/post/$', comment_post, name='comment_post'),
    # 登录表单
    url(r'^login/post/$', do_login, name='login_post'),
    # 用户注销
    url(r'^logout/post/$', do_logout, name='logout_post'),
    # 注册页面
    url(r'^reg/', do_reg, name='reg'),
]
