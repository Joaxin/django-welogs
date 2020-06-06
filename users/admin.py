from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,EmailVerifyRecord, Banner

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'nickname','link','gender','t_publish']
    list_filter = ('gender', 'email',)

    fieldsets = (
        (None, {'fields': ('email', 'password','t_publish')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('个人信息', {'fields': ('avatar', 'nickname','birthday','gender','address','mobile','link')}),
        ('微博信息', {'fields': ('fans_num', 'blog_num','follow_num','message_nums')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'index', 't_publish', 'image', 'jmp_url']
    search_fields = ['title', 'index', 'image', 'jmp_url']
    list_filter = ['title', 'index', 't_publish', 'image', 'jmp_url']


admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(Banner, BannerAdmin)