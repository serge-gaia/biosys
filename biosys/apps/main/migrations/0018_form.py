# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 01:44
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_datasetmedia_projectmedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layout', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
