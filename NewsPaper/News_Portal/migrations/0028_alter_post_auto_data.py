# Generated by Django 4.0.4 on 2022-05-24 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0027_alter_post_auto_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 5, 24, 11, 38, 46, 517648), max_length=64),
        ),
    ]
