# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 14:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('physics', '0016_auto_20170801_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='demo',
        ),
        migrations.DeleteModel(
            name='Keyword',
        ),
    ]
