# from django.shortcuts import render, get_object_or_404
# from django.views import View
# from .models import Quote, Category, Person

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from taggit.models import Tag

# from django.views.generic import ListView

# from django.shortcuts import render, get_object_or_404
# from django.views import View
# from .models import Quote, Category

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from taggit.models import Tag

import json
import os
import uuid

from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from skeleton.settings import WEB_HOST_MEDIA_URL, TEMP_IMAGE_DIR


@login_required
@csrf_exempt
def upload_temp_image(request):
    result = {}
    if request.method == 'POST':
        files = request.FILES
        if files:
            image_url_list = []
            for file_name in files:
                image_url_list.append(handle_uploaded_file(files.get(file_name)))  # 处理上传文件
            result = {'msg': 'success', "image_list": image_url_list, }

        else:
            result = {'msg': 'failed', "image_list": []}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")  # 返回json


# 处理上传的文件
def handle_uploaded_file(file):
    # 分割文件名，提取拓展名
    extension = os.path.splitext(file.name)
    # 使用uuid4重命名文件，防止重名文件相互覆盖
    # 注意首先在项目的根目录下新建media/tempimg，或者自己使用python代码创建目录
    file_name = '{}{}'.format(uuid.uuid4(), extension[1])
    with open(TEMP_IMAGE_DIR + file_name, 'wb+') as destination:
        for chunk in file.chunks():  # 防止文件太大导致内存溢出
            destination.write(chunk)
    # 返回图片的URL
    return os.path.join(WEB_HOST_MEDIA_URL, file_name)


import re

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login
from itertools import chain

# Create your views here.
from django.views.generic.base import View
from django.http import JsonResponse
from django.urls import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import MiniBlog, Topic
# from operations.models import BlogComment
# from users.models import UserProfile
# from operations.models import UserFollowed, UserFav, UserGood, UserMessage
# from .forms import BlogContentForm, SearchContentForm

# 当用户登录时，返回其关注的人的微博，没登录返回所有微博
class MainpageView(View):
    def get(self, request):
        all_blogs = MiniBlog.published.all().order_by('-t_publish')

        paginator = Paginator(all_blogs, 5) 
        page = request.GET.get('page')
        # 进行分页传递
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        all_topic = Topic.objects.all().order_by('-topic_blogs_num')[:10]

        if request.user.is_authenticated:
            return render(request, 'aphor/stella.html', {'page': page,'blogs': blogs, 'all_topic': all_topic})
        else:
            return render(request, 'aphor/stella.html', {'page': page,'blogs': "请登录", 'all_topic': all_topic})

# from op.models import BlogComment
# class BlogTextPageView(View):
#     def get(self, request, blog_id):
#         blog = MiniBlog.objects.get(id=int(blog_id))
#         blog.num_click += 1
#         blog.save()
#         # return HttpResponse("to be continued for your work微博+评论区")
#         # （新增）
#         comments = BlogComment.objects.filter(blog=blog)
#         return render(request, 'aphor/stella_detail.html', {
#             'blog': blog,
#             'comments': comments
#         })

from .forms import BlogContentForm
class SendBlogView(View):
    def post(self, request):
        blog_form = BlogContentForm(request.POST, request.FILES or None)
        if blog_form.is_valid():
            blog = MiniBlog()
            
            print(blog.id)

            blog.user = request.user
            blog.content = request.POST.get("content", "")
            blog.image = blog_form.cleaned_data["image"]
            if blog.image:
                blog.has_pic = 1

            # 替换@用户
            re_str = blog.content
            users_list = []
            users_str = re.findall(r'@(.+?)\s', re_str)

            users_str_1 = re.findall(r'^(.+?)@', re_str[::-1])
            if users_str_1:
                users_str.append(users_str_1[0][::-1])

            for user_str in users_str:
                user = UserProfile.objects.filter(nickname=user_str)
                if user:
                    users_list.append(user[0])
                    re_str = re_str.replace('@' + user_str,
                                            '<a href="/user/' + str(user[0].id) + '/">' + '@' + user_str + '</a>')
            blog.content = re_str

            blog.save()
            print(blog.id)

            # 新建@提醒
            for user in users_list:
                message = UserMessage()
                message.user = user
                message.blog_id = blog.id
                message.save()

                user.message_nums = UserMessage.objects.filter(user=user, has_read=False).count()
                user.save()

            # blog_form.save()
            # self.topic_test(blog.content, blog)

            # 替换话题
            # re_str = blog.content
            # topics_str = re.findall(r'#(.+?)#', re_str)
            # for topic_str in topics_str:
            #     topic = Topic.objects.filter(topic_name=topic_str)
            #     if topic:
            #         re_str = re_str.replace('#' + topic_str + '#', '<a href="/weibo/topic/' + str(
            #             topic[0].id) + '">' + '#' + topic_str + '#' + '</a>')

            # blog.content = re_str
            blog.save()
            return HttpResponseRedirect(reverse('aphor:mainpage'))


# # def quote_list(request):
# #     object_list = Quote.published.all()
# #     paginator = Paginator(object_list, 3)  # 每页显示3篇文章
# #     page = request.GET.get('page')
# #     try:
# #         quotes = paginator.page(page)
# #     except PageNotAnInteger:
# #         # 如果page参数不是一个整数就返回第一页
# #         quotes = paginator.page(1)
# #     except EmptyPage:
# #         # 如果页数超出总页数就返回最后一页
# #         quotes = paginator.page(paginator.num_pages)
# #     return render(request, 'aphor/quote/list.html', {'page': page, 'quotes': quotes})

# from django.views.generic import ListView

# class QuoteListView(ListView):
#     queryset = Quote.published.all() # 实际上，可以不使用这个变量，通过指定model = Quote，这个CBV就会去进行Quote.objects.all()查询获得全部文章。
#     # 如果不设置context_object_name参数，默认的变量名称是object_list
#     context_object_name = 'quotes'
#     paginate_by = 10
#     template_name = 'aphor/list.html'

# def quote_list(request, tag_slug=None):
#     object_list = Quote.published.all()
#     tag = None

#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         object_list = object_list.filter(tags__in=[tag])

#     paginator = Paginator(object_list, 20) # 3 quotes in each page
#     page = request.GET.get('page')
#     try:
#         quotes = paginator.page(page)
#     except PageNotAnInteger:
#         quotes = paginator.page(1)
#     except EmptyPage:
#         quotes = paginator.page(paginator.num_pages)

#     return render(request, 'aphor/list.html', {'page': page, 'quotes': quotes, 'tag': tag})


# from .models import Quote, Comment
# from .forms import EmailQuoteForm, CommentForm
# from django.db.models import Count

# # 一些相同主题的文章会具有相同的标签，可以创建一个功能给用户按照共同标签数量的多少推荐文章。
# # 为了实现该功能，需要如下几步：

# # 获得当前文章的所有标签
# # 拿到所有具备这些标签的文章
# # 把当前文章从这个文章列表里去掉以避免重复显示
# # 按照具有相同标签的多少来排列
# # 如果文章具有相同数量的标签，按照时间来排列
# # 限制总推荐文章数目


# def quote_detail(request, quote_id, quote):
#     quote = get_object_or_404(Quote, slug=quote, status="published",  id=quote_id)
#     # 列出文章对应的所有活动的评论
#     comments = quote.comments.filter(active=True)
#     # 以Comments类中定义的外键的related_name属性的名称作为管理器，对quote对象执行查询从而得到了所需的QuerySet。
    
#     # 新增评论的功能, 初始化了一个new_comment变量为None，用于标记一个新评论是否被创建。
#     new_comment = None

#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # 通过表单直接创建新数据对象，但是不要保存到数据库中
#             # commit=False，则数据对象会被创建但不会被写入数据库，便于在保存到数据库之前对对象进行一些操作
#             new_comment = comment_form.save(commit=False)
#             # 设置外键为当前文章
#             new_comment.quote = quote
#             # 将评论数据对象写入数据库
#             new_comment.save()
#             # save()方法仅对ModelForm生效，因为Form类没有关联到任何数据模型。
#     else:
#         comment_form = CommentForm()  # 创建空白表单

#     # 显示相近Tag的文章列表
#     quote_tags_ids = quote.tags.values_list('id',flat=True)
#     # 选出所有包含上述标签的文章并且排除当前文章
#     similar_tags = Quote.published.filter(tags__in=quote_tags_ids).exclude(id=quote.id)
#     similar_quotes = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags','-t_publish')[:4]
#     return render(request, 'aphor/detail.html',
#                   {'quote': quote,
#                   'comments': comments,
#                   'new_comment': new_comment,
#                   'comment_form': comment_form,
#                   'similar_quotes': similar_quotes})




# from .forms import EmailQuoteForm,SearchForm

# from django.core.mail import send_mail
# def quote_share(request, quote_id, quote):
#     # 通过id 获取 quote 对象
#     quote = get_object_or_404(Quote, slug=quote, id=quote_id, status='published')
#     sent = False

#     if request.method == "POST":
#         # 表单被提交
#         form = EmailQuoteForm(request.POST)
#         if form.is_valid():
#             # 表单字段通过验证
#             cd = form.cleaned_data
#             quote_url = request.build_absolute_uri(quote.get_absolute_url())
#             subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], quote.title)
#             message = 'Read "{}" at <a href="{}"></a> \n\n{}\'s comments:{}'.format(quote.title, quote_url, cd['name'], cd['comments'])
#             send_mail(subject, message, 'llsites@163.com', [cd['to']], fail_silently=False)
#             sent = True

#     else:
#         form = EmailQuoteForm()
#     return render(request, 'aphor/share.html', {'quote': quote, 'form': form, 'sent': sent})

# # from django.contrib.quotegres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
# # def quote_search(request):
# #     form = SearchForm()
# #     query = None
# #     results = []
# #     if 'query' in request.GET:
# #         form = SearchForm(request.GET)
# #         if form.is_valid():
# #             query = form.cleaned_data['query']
# #             results = Quote.objects.annotate(
# #                 similarity=TrigramSimilarity('title', query),
# #             ).filter(similarity__gt=0.3).order_by('-similarity')
# #     return render(request,
# #                   'aphor/search.html',
# #                   {'form': form,
# #                    'query': query,
# #                    'results': results})
# # from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.urls import reverse_lazy
# # from django.views import generic
# # from django.contrib.messages.views import SuccessMessageMixin

# # from aphor.models import Quote, Person, Category


# # Create your views here.
# # class Master(generic.ListView):
# #     def get_context_data(self, *, object_list=None, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context['persons_widget'] = Person.objects.all()
# #         context['categories_widget'] = Category.objects.all()
# #         return context


# # class Index(Master):
# #     model = Quote
# #     ordering = ['-pk']
# #     paginate_by = 1
# #     context_object_name = 'quotes_object_list'
# #     template_name = 'index.html'


# # class Persons(Master):
# #     model = Person
# #     paginate_by = 1
# #     context_object_name = 'persons_object_list'
# #     template_name = 'persons.html'


# # class Random(Index):
# #     paginate_by = False

# #     def get_queryset(self):
# #         return Quote.objects.order_by("?")[:10]


# # class QuotesByPerson(Index):
# #     def get_queryset(self):
# #         return Quote.objects.filter(person=self.kwargs['person_pk'])


# # class QuotesByCategory(Index):
# #     def get_queryset(self):
# #         return Quote.objects.filter(category=self.kwargs['category_pk'])


# def QuotesByCategory(request, category_pk):
#     category = get_object_or_404(Category, pk=category_pk)

#     object_list = Quote.published.filter(category_id = category_pk)

#     paginator = Paginator(object_list, 20) # 3 quotes in each page
#     page = request.GET.get('page')
#     try:
#         quotes = paginator.page(page)
#     except PageNotAnInteger:
#         quotes = paginator.page(1)
#     except EmptyPage:
#         quotes = paginator.page(paginator.num_pages)

#     return render(request, 'aphor/list.html', {'page': page, 'quotes': quotes, 'category': category, 'tag':None})
# # class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView, Master):
# #     fields = ["title"]
# #     model = Category
# #     success_url = '/create/category'
# #     success_message = "Category was created successfully"


# # class PersonCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView, Master):
# #     fields = ["full_name", "biography", "picture"]
# #     model = Person
# #     success_url = '/create/person'
# #     success_message = 'Person was created successfully'


# # class QuoteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView, Master):
# #     fields = ["person", "category", "content"]
# #     model = Quote
# #     success_url = '/create/quote'
# #     success_message = 'Quote was created successfully'
