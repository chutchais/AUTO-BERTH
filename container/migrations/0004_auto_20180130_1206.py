# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-30 12:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('container', '0003_dischargeport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='dis_port',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='container.DischargePort'),
        ),
    ]