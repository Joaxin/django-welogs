from django.db import models
from django.utils import timezone
from django.conf import settings 
from django.urls import reverse
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from slugify import slugify
# from users.models import CustomUser

# Create your models here.

# _*_ coding: utf-8 _*_

import os
import shutil
# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import ClearableFileInput, ModelForm, forms, TextInput
from django.template import loader
from django import forms
from django.utils.safestring import mark_safe

from skeleton.settings import MEDIA_ROOT, WEB_HOST_MEDIA_URL, TEMP_IMAGE_DIR, MODEL_IMAGE_DIR, MODEL_MEDIA_URL

class ImageInput(ClearableFileInput):
    template_name = "aphor/img_upload.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class UploadImageList(TextInput):
    template_name = "aphor/img_upload_list.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class UploadModel(models.Model):
    images = models.FileField('图片', upload_to="static/upload_multi_img/")
    images_list = models.CharField('', max_length=10000)

    def save(self, *args, **kwargs):
        # 阻止images字段的数据保存在数据库中，因为我们不需要
        self.images = ""
        model_images = []
        # print(self.images_list)
        # 将暂存目录中的图片转存到正式目录
        for root, dirs, files in os.walk(TEMP_IMAGE_DIR):
            # print('files:', files)
            for file in files:
                if os.path.join(WEB_HOST_MEDIA_URL, file) in self.images_list:
                    shutil.move(TEMP_IMAGE_DIR + file, MODEL_IMAGE_DIR + file)
                    model_images.append(os.path.join(MODEL_MEDIA_URL, file))

        # 清空暂存目录下所有图片
        shutil.rmtree(TEMP_IMAGE_DIR)
        os.mkdir(TEMP_IMAGE_DIR)
        # 将模型原来的图片URL换为存到正式目录后的URL
        self.images_list = str(model_images).replace('[', "").replace(']', '')
        # 必须调用父类的方法，否则数据不会保存
        super().save(*args, **kwargs)


# 删除被删除的模型的图片
@receiver(post_delete, sender=UploadModel)
def delete_upload_files(sender, instance, **kwargs):
    image_list = getattr(instance, 'images_list', '')

    if not image_list:
        return
    else:
        # 去除image_list中URL存在的''字符
        list = image_list.replace("'", "").replace("'", "").split(",")
        # print("000000", list)
        # 删除被删除的模型的图片
        for image in list:
            # 获取文件名
            delete_image_name = image.split('/')[-1]
            # print("9999999", delete_image_name)
            os.remove(MODEL_IMAGE_DIR + delete_image_name)


class UploadForm(ModelForm):
    images = forms.FileField(label="图片", widget=ImageInput, help_text="按住ctrl多选,最多9张", required=False)
    images_list = forms.CharField(label='', widget=UploadImageList, help_text='', required=False)

    class Meta:
        model = UploadModel
        fields = ['images', 'images_list']



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(default="", max_length=50, verbose_name="话题名称")
    topic_blogs_num = models.IntegerField(verbose_name="相关微博数", default=0, null=True, blank=True)
    t_publish = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "微博话题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topic_name[:20]

class MiniBlog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="发布用戶",
                             related_name='miniblog_set',default=1)
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    status = models.CharField(verbose_name='发布状态',max_length=10, choices=STATUS_CHOICES, default='published')

    t_publish = models.DateTimeField(verbose_name='发布时间',default=timezone.now)
    t_update = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    content = MarkdownxField(verbose_name="正文 :", blank=True, max_length=2500)

    tags = TaggableManager()

    images = models.ForeignKey(UploadModel, on_delete=models.CASCADE, verbose_name="图集", null=True, blank=True )

    num_click = models.IntegerField(verbose_name="微博点击数", default=0, null=True, blank=True)
    num_likes = models.IntegerField(verbose_name="点赞数", default=0, null=True, blank=True)
    num_comment = models.IntegerField(verbose_name="评论数", default=0, null=True, blank=True)
    num_fav= models.IntegerField(verbose_name="收藏数", default=0, null=True, blank=True)

    has_pic = models.IntegerField(verbose_name="是否有图", default=0, null=True, blank=True)

    need_unfold = models.IntegerField(choices=((0, "不需展开"), (1, "需要展开且未展开"), (2, "需展开且已展开")), default = 0)

    related_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, verbose_name="微博相关话题")

    objects = models.Manager()  # 默认的管理器
    published = PublishedManager()  # 自定义管理器

    class Meta:
        verbose_name = "微博"
        verbose_name_plural = verbose_name
        ordering = ('-t_publish',)

    def __str__(self):
        return '{} - {} ： {}'.format(self.user,self.t_publish, self.content[:25])

    def shorttext(self):
        return self.content[:10] + "..."

    def judgefold(self):
        foldlen = 5
        if len(self.content) < foldlen:
            self.need_unfold = 0  # 不需展开
        else:
            self.need_unfold = 1

