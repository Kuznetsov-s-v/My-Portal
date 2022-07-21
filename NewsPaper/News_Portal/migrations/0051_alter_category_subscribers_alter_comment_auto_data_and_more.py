# Generated by Django 4.0.4 on 2022-07-21 21:48

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('News_Portal', '0050_alter_comment_auto_data_alter_post_auto_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(null=True, through='News_Portal.CategoryUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 7, 22, 0, 48, 11, 76497), max_length=64),
        ),
        migrations.AlterField(
            model_name='post',
            name='auto_data',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 22, 0, 48, 11, 74496), max_length=64),
        ),
    ]