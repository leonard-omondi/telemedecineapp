# Generated by Django 3.2.7 on 2021-11-15 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telemedicine', '0002_auto_20211113_2231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='user',
            table='telemedicine_user1',
        ),
    ]
