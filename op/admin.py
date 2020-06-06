# _*_ coding:utf-8 _*_
from django.contrib import admin
from .models import UserGood, UserFav, UserFollowed, UserMessage


# 设置MiniBlog在界面中的显示
class UserGoodAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 't_publish']
    search_fields = ['user', 'blog']
    list_filter = ['user', 'blog', 't_publish']


class UserFavAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 't_publish']
    search_fields = ['user', 'blog']
    list_filter = ['user', 'blog', 't_publish']


class UserFollowedAdmin(admin.ModelAdmin):
    list_display = ['user', 'follow_user', 't_publish']
    search_fields = ['user', 'follow_user']
    list_filter = ['user', 'follow_user', 't_publish']


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'has_read', 't_publish']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 't_publish']


# 注册model
admin.site.register(UserGood, UserGoodAdmin)
admin.site.register(UserFav, UserFavAdmin)
admin.site.register(UserFollowed, UserFollowedAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
