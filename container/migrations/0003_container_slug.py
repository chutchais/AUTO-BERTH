# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('container', '0002_auto_20171226_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]