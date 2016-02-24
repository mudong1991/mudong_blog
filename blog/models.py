# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
# Create your models here.


# 用户模型
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.jpg',
                               max_length=200, blank=True, null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, null=True, blank=True, verbose_name='QQ号')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号', unique=True)
    url = models.CharField(max_length=100, blank=True, null=True, verbose_name='个人网站网址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 文章类别
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(verbose_name='显示顺序(从小到大)', default=99)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='文章标题')
    desc = models.CharField(max_length=500, verbose_name='文章描述', blank=True, null=True)
    content = models.TextField(verbose_name='文章内容')
    url = models.URLField(blank=True, null=True, verbose_name='文章链接')
    portal = models.ImageField(upload_to='article/%Y/%m', default='article/default.jpg', null=True
                               , blank=True, max_length=1000, verbose_name='文章图片')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    is_recommed = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='发表时间')
    # timezone.now可以保存正确的时间，已经后台可以正常显示修改
    user = models.ForeignKey(User, verbose_name='用户')
    category = models.ForeignKey(Category, verbose_name='分类', blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']
        permissions = [('can_view', "Can see article"),
                       ('can_add', "Can add article"),
                       ('can_edit', "Can edit article"),
                       ('can_delete', "Can delete article")]

    def __unicode__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name="邮箱地址" )
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name="个人网页地址")
    date_publish = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='用户')
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return str(self.id)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    index = models.IntegerField(default=99, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title

