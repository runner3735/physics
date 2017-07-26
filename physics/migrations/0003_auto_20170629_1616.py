# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 20:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('physics', '0002_auto_20170629_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='demo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physics.Demo'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='demo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physics.Demo'),
        ),
    ]
