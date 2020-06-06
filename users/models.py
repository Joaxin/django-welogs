from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
#用pillow、django-imagekit模块设置图片，可以处理图片，生成指定大小的缩略图，前端显示src="{{ user.avatar.url }}
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

#扩展Django自带的User模型字
#扩展Django自带的User模型字
# 继承 AbstractUser ，django 自带用户类，可扩展用户个人信息，AbstractUser 模块下有：password,username、first_name、last_name、email、last_login,is_superuser,is_staff,is_active,date_joined
class CustomUser(AbstractUser):
  
    nickname = models.CharField(max_length=30, blank=True, null=True, verbose_name='昵称')
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('U','保密')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,verbose_name="性别",
                              default='U')
    address = models.CharField(max_length=200, verbose_name="地址", null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")
    # 扩展用户个人网站字段
    link = models.URLField('个人网址', blank=True, help_text='提示：网址必须填写以http开头的完整形式')
    # 扩展用户头像字段,upload_to后必须是相对路径,上传路径已设置为media，保存的是图片地址，前端user.avatar.url获取
    avatar = ProcessedImageField(upload_to='avatar',default='avatar/default.png',verbose_name='头像',
                                processors=[ResizeToFill(100, 100)], # 处理后的图像大小
                                format='JPEG', # 处理后的图片格式
                                options={'quality': 95} # 处理后的图片质量
                                )
    fans_num = models.IntegerField(verbose_name="粉丝数", default=0)
    blog_num = models.IntegerField(verbose_name="微博数", default=0)
    follow_num = models.IntegerField(verbose_name="关注数", default=0)
    t_publish = models.DateField(default=datetime.now, verbose_name="加入时间")
    message_nums = models.IntegerField(verbose_name='未读消息数', default=0)
     #定义手动保存图（IIS下User.save()保存失败）
    def save_avatar(self,upload_image):
        import os
        import uuid
        from django.conf import settings
        #创建与用户名的文件夹
        upload_path=os.path.join(settings.MEDIA_ROOT,'avatar',self.username)
        if not upload_path:
          try:
            os.makedirs(new_path)
          except:
            pass
        # 生成一个随机字符串
        uuid_str_name = uuid.uuid4().hex+'.jpg'
        #保存
        with open(os.path.join(upload_path,uuid_str_name), 'wb+') as file:
          for chunk in upload_image.chunks():
              file.write(chunk)
          return uuid_str_name

    #显示用户的邮箱是否验证过，并提醒他们去验证邮箱
    def account_verified(self):
        if self.user.is_authenticated: #django的auth系统功能，只能利用django自己的登陆方法才能判断用户是否登录
          result = EmailAddress.objects.filter(email=self.user.email)
        if len(result):
          return result[0].verified
        return False

    # 定义网站管理后台表名
    class Meta:
        verbose_name = '用户信息' 
        verbose_name_plural = verbose_name #指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’
        ordering = ['-id']
        #admin后台显示名字关联到此表的字段的后天显示名字
    def __str__(self):
        return self.username

# 邮箱验证码类
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="邮箱验证码")
    email = models.CharField(max_length=40, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("findback", "找回密码")), max_length=20)
    send_time = models.DateField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.code, self.email)


# 未登录页轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    index = models.IntegerField(default=1000, verbose_name="播放顺序")
    t_publish = models.DateField(default=datetime.now, verbose_name="添加时间")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=100)
    jmp_url = models.URLField(max_length=200, verbose_name="跳转地址")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title