# -*- coding:utf-8 -*-
from django.contrib import admin
from blog.models import *


# 文章模型admin显示管理
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content', 'url', 'portal', 'date_publish', 'category', 'tag', 'user'),
        }),
        ('高级选项',{
            'classes': ('collapse',),
            'fields': ('click_count', 'like_count', 'is_recommed'),
        })
    )

    # 格式化显示时间
    def time_publish(self, obj):
        return obj.date_publish.strftime('%Y年%m月%d日 %H:%M:%S')
    time_publish.admin_order_field = 'date_publish'
    time_publish.short_description = '发布时间'

    # 定义文章list显示项目
    list_display = ('title', 'desc', 'time_publish', 'click_count')
    list_editable = ('click_count',)

    # 引入媒体文件，创建富文本
    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )

# Register your models here.
admin.site.register(User)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Ad)
admin.site.register(Links)