# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-25 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bayplan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bayplanfile',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='bayplanfile',
            name='filename',
            field=models.FileField(blank=True, null=True, upload_to='bayplan/%Y/%m/%d/'),
        ),
    ]
