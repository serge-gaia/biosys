# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vegetation', '0010_auto_20160421_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stratumspecies',
            name='collector_no',
            field=models.CharField(blank=True, max_length=200, verbose_name='Collector No'),
        ),
    ]