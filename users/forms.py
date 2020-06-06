from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('nickname','link','avatar',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class ProfileForm(forms.Form):
    class Meta:
        # 关联的数据库模型，这里是用户模型
        model = CustomUser
        # 前端显示、可以修改的字段（admin中）
        fields = ['nickname','link', 'avatar']