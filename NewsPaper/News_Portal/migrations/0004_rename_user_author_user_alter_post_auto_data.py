# Generated by Django 4.0.4 on 2022-05-21 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0003_rename_user_author_user_alter_post_auto_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='User',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 5, 21, 14, 56, 18, 47122), max_length=64),
        ),
    ]
