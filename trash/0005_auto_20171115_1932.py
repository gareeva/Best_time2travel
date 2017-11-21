# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 19:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_auto_20171115_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=1000)),
                ('short_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='city_country',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='places.Country'),
            preserve_default=False,
        ),
    ]
