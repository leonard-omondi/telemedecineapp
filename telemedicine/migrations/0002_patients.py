# Generated by Django 3.2.7 on 2021-09-19 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemedicine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssn', models.PositiveIntegerField()),
                ('lastname', models.CharField(max_length=50)),
                ('firstname', models.CharField(max_length=50)),
                ('middlename', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('height', models.FloatField(max_length=4)),
                ('weight', models.FloatField(max_length=4)),
                ('gender', models.CharField(choices=[('f', 'female'), ('m', 'male')], max_length=1)),
                ('ethnicity', models.CharField(max_length=20)),
                ('job', models.CharField(max_length=50)),
                ('smoking', models.BooleanField()),
                ('familyhistory', models.TextField()),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(max_length=2)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
    ]