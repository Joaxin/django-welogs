import json
import base64
from django.shortcuts import render
from django.http import HttpResponse

from . import models
# Create your views here.

# auth中用户权限有关的类。auth可以设置每个用户的权限。
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# 使用login_required装饰器，用户只有登录了才能访问其用户资料


@login_required
def profile(request):
    # AUTH_USER_MODEL 类型的对象，表示当前登录的用户。
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


@login_required  # 使用login_required装饰器，用户只有登录了才能访问其用户资料
@csrf_exempt  # 取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
def profile_update(request):
    # request.is_ajax(): #判断请求头中是否含有X-Requested-With的值
    if request.is_ajax():
        # request.POST.get('')不存在默认为空，request.POST[]不存在报错
        key = request.POST.get('key')
    if key == 'link':
        link = request.POST['link']
        username = request.POST['username']
        models.CustomUser.objects.filter(email=username).update(link=link)
        link = models.CustomUser.objects.filter(email=username).first().link
        linkJson = {'link': link}
        return HttpResponse(json.dumps(linkJson))

    elif key == 'avatar':
        username = request.POST['username']
        # 用ModelForm可代替手动编写代码存储上传文件
        user_profile = models.CustomUser.objects.filter(email=username).first()
        user_profile.avatar = request.FILES.get('avatar')
        user_profile.save()
        url = user_profile.avatar.url
        dataJson = {'url': url}
    return HttpResponse(json.dumps(dataJson))
