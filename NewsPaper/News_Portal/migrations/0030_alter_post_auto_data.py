# Generated by Django 4.0.4 on 2022-05-24 20:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0029_alter_post_auto_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='auto_data',
            field=models.CharField(default=datetime.datetime(2022, 5, 24, 23, 2, 47, 367132), max_length=64),
        ),
    ]
