# Generated by Django 4.0.4 on 2022-05-23 11:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('News_Portal', '0009_remove_comment_comment_user_comment_comment_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_user',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 5, 23, 14, 23, 43, 96159), max_length=64),
        ),
    ]
