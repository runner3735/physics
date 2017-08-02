# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-01 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('physics', '0014_auto_20170731_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photonote',
            name='contributor',
        ),
        migrations.RemoveField(
            model_name='photonote',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='note',
            name='demo',
        ),
        migrations.AddField(
            model_name='demo',
            name='notes',
            field=models.ManyToManyField(to='physics.Note'),
        ),
        migrations.AddField(
            model_name='photo',
            name='notes',
            field=models.ManyToManyField(to='physics.Note'),
        ),
        migrations.AlterField(
            model_name='demo',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.DeleteModel(
            name='PhotoNote',
        ),
    ]