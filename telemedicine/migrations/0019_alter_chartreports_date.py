# Generated by Django 3.2.7 on 2021-12-04 01:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemedicine', '0018_auto_20211203_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartreports',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 3, 20, 3, 34, 888563)),
        ),
    ]