# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-19 15:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_remove_country_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='country_name',
        ),
    ]
