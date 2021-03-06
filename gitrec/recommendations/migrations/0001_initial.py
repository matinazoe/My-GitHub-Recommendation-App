# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 13:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(default='https://github.com/personal')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='date updated')),
                ('forked_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recommendations.Project')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owns', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
        migrations.CreateModel(
            name='Project_Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_code_of', to='recommendations.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Project_members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('repo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_made', to='recommendations.Project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250, null=True)),
                ('slug', models.SlugField(max_length=250, null=True, unique_for_date='pub_date')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('reviewed', 'Reviewed')], default='draft', max_length=10)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('comment', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('Reviewtags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated', to='recommendations.Project')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Watchers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('repo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_watched', to='recommendations.Project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
