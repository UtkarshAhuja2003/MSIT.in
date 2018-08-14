# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-19 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0012_auto_20180319_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchrecord',
            name='year',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
