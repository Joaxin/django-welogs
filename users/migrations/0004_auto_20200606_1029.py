# Generated by Django 3.0.6 on 2020-06-06 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200606_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='地址'),
        ),
    ]
