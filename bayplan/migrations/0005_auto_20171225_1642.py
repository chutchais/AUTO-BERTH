# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-25 16:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bayplan', '0004_auto_20171225_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='bayPlanfile',
        ),
        migrations.RemoveField(
            model_name='container',
            name='user',
        ),
        migrations.DeleteModel(
            name='Container',
        ),
    ]