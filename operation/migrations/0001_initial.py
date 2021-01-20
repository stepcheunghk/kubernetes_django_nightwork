# Generated by Django 3.0.4 on 2020-03-22 15:00

import datetime
from django.db import migrations, models
import operation.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('category', models.CharField(default='D', max_length=255)),
                ('startdate', models.DateField()),
                ('starttime', models.TimeField(default=datetime.time(0, 0))),
                ('enddate', models.DateField()),
                ('endtime', models.TimeField(default=datetime.time(5, 0))),
                ('duration', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('subject', models.TextField()),
                ('reason_type', models.CharField(max_length=255)),
                ('reason', models.TextField()),
                ('impact', models.TextField(default='No Service Impact')),
                ('remarks', models.CharField(default='N/A', max_length=255)),
                ('vendor', models.CharField(max_length=255)),
                ('vendor_phone', models.CharField(max_length=255)),
                ('mop', models.FileField(blank=True, null=True, upload_to=operation.models.filename)),
            ],
        ),
    ]
