# Generated by Django 4.0.4 on 2022-05-24 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0021_alter_post_auto_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 5, 24, 10, 9, 52, 820352), max_length=64),
        ),
    ]
