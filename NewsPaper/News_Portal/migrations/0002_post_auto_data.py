# Generated by Django 4.0.4 on 2022-05-21 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 5, 21, 11, 38, 27, 627162), max_length=64),
        ),
    ]
