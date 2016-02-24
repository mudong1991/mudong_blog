# -*- coding:utf-8 -*-
from django import template

register = template.Library()


# 自定义一个时间过滤器，讲月份转换成大写
# @register.filter(name='aaa')
def month_to_upper(key):
    return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][key.month - 1]


# 将自定义的过滤器注册
register.filter('mouth_to_upper', month_to_upper)
