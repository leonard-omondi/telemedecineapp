# Generated by Django 3.2.7 on 2021-12-04 01:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telemedicine', '0019_alter_chartreports_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartreports',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 3, 20, 57, 2, 159630)),
        ),
        migrations.AlterField(
            model_name='patients',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]