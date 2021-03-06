# Generated by Django 3.0.6 on 2020-06-06 01:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aphor', '0005_auto_20200605_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500, verbose_name='消息内容')),
                ('has_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('t_publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('blog_id', models.IntegerField(default=0, verbose_name='微博id')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='接收用户')),
            ],
            options={
                'verbose_name': '用户消息',
                'verbose_name_plural': '用户消息',
            },
        ),
        migrations.CreateModel(
            name='UserGood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='点赞时间')),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aphor.MiniBlog', verbose_name='被点赞微博')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞用户')),
            ],
            options={
                'verbose_name': '用户点赞',
                'verbose_name_plural': '用户点赞',
            },
        ),
        migrations.CreateModel(
            name='UserFollowed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followUser_id', models.IntegerField(default=0, verbose_name='被关注用户id')),
                ('t_publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='关注时间')),
                ('follow_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关注其的用户')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fans_set', to=settings.AUTH_USER_MODEL, verbose_name='被关注的用户')),
            ],
            options={
                'verbose_name': '用户关注',
                'verbose_name_plural': '用户关注',
            },
        ),
        migrations.CreateModel(
            name='UserFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间')),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aphor.MiniBlog', verbose_name='被收藏微博')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='收藏用户')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', markdownx.models.MarkdownxField(blank=True, max_length=2500, verbose_name='正文 :')),
                ('t_publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aphor.MiniBlog', verbose_name='微博')),
                ('reply_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_user', to=settings.AUTH_USER_MODEL, verbose_name='评论的人')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
