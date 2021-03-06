# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0007_auto_20160716_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='review',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='recommendations.Project'),
        ),
    ]
