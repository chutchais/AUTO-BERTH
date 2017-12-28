# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-25 10:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('berth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BayPlanFile',
            fields=[
                ('voy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='berth.Voy')),
                ('filename', models.FileField(upload_to='bayplan/%Y/%m/%d/')),
                ('remark', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]