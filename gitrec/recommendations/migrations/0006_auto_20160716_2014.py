# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0005_auto_20160714_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]