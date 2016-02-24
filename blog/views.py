# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from blog.models import *
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
import logging
from forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password

# Create your views here.
# 定义一个日志器
logger = logging.getLogger('blog.views')


# 定义全局变量函数字典，并设置到settings中
def global_setting(request):
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_KEYWORDS = settings.SITE_KEYWORDS
    SITE_DESC = settings.SITE_DESC
    SITE_AUTHOR = settings.SITE_AUTHOR
    WEIBO_XINLANG = settings.WEIBO_XINLANG
    WEIBO_TENGXUN = settings.WEIBO_TENGXUN
    TIEBA_BAIDU = settings.TIEBA_BAIDU
    WEIXIN_HAO = settings.WEIXIN_HAO
    LIANXI_EMAIL = settings.LIANXI_EMAIL
    LIANXI_QQ = settings.LIANXI_QQ

    # 首页欢迎信息title
    title_index = settings.SITE_INDEX_TITLE
    # 分类类别
    category_list_nav = Category.objects.all()[:10]
    # 侧边栏分类
    category_list_right = Category.objects.all()[:6]
    # 侧边栏推荐文章
    article_recommed_list_right = Article.objects.filter(is_recommed=True)[:6]
    # 侧边标签
    tag_list_right = Tag.objects.all()[:25]
    # 页脚友情链接
    links_list = Links.objects.all()[:20]

    return locals()


# title是每个页面的标题名字(首页的标题唯一)

# 首页
def index(request):
    try:
        title = settings.SITE_INDEX_TITLE
        # 文章数据获取
        article_list = Article.objects.all()[:10]
        # 文章分页
        article_list = getPage(request, article_list)
        article_list_num_pages = range(1, article_list.paginator.num_pages+1)
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())


# 分类导航页
def category(request, category_name):
    try:
        try:
            category = Category.objects.get(name=category_name)
        except category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        # 获取分类name
        title = '慕冬博客-' + category.name.encode('utf-8')  # category_name是Unicode编码要转换成utf-8
        # 获取分类文章列表
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
        # 分页的页码列表
        article_list_num_pages = range(1, article_list.paginator.num_pages+1)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())


# 分类导航页
def tag(request, tag_name):
    try:
        try:
            tag = Tag.objects.get(name=tag_name)
        except tag.DoesNotExist:
            return render(request, 'failure.html', {'reason': '标签不存在'})
        # 获取分类name
        title = '标签-' + tag.name.encode('utf-8')  # tag_name是Unicode编码要转换成utf-8
        # 获取分类文章列表
        article_list = Article.objects.filter(tag=tag)
        article_list = getPage(request, article_list)
        # 分页的页码列表
        article_list_num_pages = range(1, article_list.paginator.num_pages+1)
    except Exception as e:
        logger.error(e)
    return render(request, 'tag.html', locals())


# 搜索
def search(request):
    try:
        search_words = request.POST.get('keywords', None)
        title = '搜索结果-'+search_words.encode('utf-8')
        # 获取分类文章列表
        article_list = Article.objects.filter(title__contains=search_words) | Article.objects.filter(content__contains=search_words)
        article_list = getPage(request, article_list)
        # 分页的页码列表
        article_list_num_pages = range(1, article_list.paginator.num_pages+1)
    except Exception as e:
        logger.error(e)
    return render(request, 'search.html', locals())


# 文章详情页
def article(request):
    try:
        try:
            # 获取文章的id
            id = request.GET.get('id', None)
            # 获取文章信息
            article = Article.objects.get(pk=id)
            title = article.title
            # 上一篇和下一篇文章
            if int(id) > 1:
                article_previous = Article.objects.get(pk=int(id) - 1)  # 上一篇文章
            else:
                article_previous = None
            if int(id) < len(Article.objects.all()):
                article_next = Article.objects.get(pk=int(id) + 1)  # 下一篇文章
            else:
                article_next = None
            # 推荐文章
            article_recommed_list = (Article.objects.filter(tag=article.tag.all) | \
                                     Article.objects.filter(is_recommed=True)).exclude(pk=id)[:12]

        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '对不起,没有找到对应的文章'})

        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_num = len(Comment.objects.annotate(comment_count=Count('article')).filter(article=article))
        comment_list = []   # 用来装父级评论
        for comment in comments:
            if comment.pid is None:
                comment_list.append(comment)
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else {'article': id})
        # 登录表单
        login_form = LoginForm({'username': request.user.username,
                                'password': request.user.password} if request.user.is_authenticated() else {})
    except Exception as e:
        logger.error(e)
    return render(request, 'article.html', locals())


# 用户登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 用户注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注册表单
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST, request.FILES)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data['username'],
                                           email=reg_form.cleaned_data['email'],
                                           url=reg_form.cleaned_data['url'],
                                           password=make_password(reg_form.cleaned_data['password']),
                                           avatar=reg_form.cleaned_data['avatar'],)
                user.save()
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            title = '注册-慕冬博客会员'
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


# 评论提交
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 获取表单数据
            comment = Comment.objects.create(username=comment_form.cleaned_data['author'],
                                             email=comment_form.cleaned_data['email'],
                                             url=comment_form.cleaned_data['url'],
                                             content=comment_form.cleaned_data['comment'],
                                             article_id=comment_form.cleaned_data['article'],
                                             pid=None,
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 4)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)  # 如果用户输入错误的page数返回第一个页
    return article_list

