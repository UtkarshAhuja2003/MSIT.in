# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-27 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_studentsociety_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsociety',
            name='order',
            field=models.CharField(max_length=20),
        ),
    ]
