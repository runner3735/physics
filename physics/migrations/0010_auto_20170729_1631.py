# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('physics', '0009_note_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['text'],
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demo',
            name='modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photonote',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='demo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physics.Demo'),
        ),
    ]
