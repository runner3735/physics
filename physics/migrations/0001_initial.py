# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 20:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Demo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mainphoto', models.IntegerField(blank=True, editable=False, null=True)),
                ('description', models.TextField(blank=True, max_length=2048)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('course', models.ManyToManyField(to='physics.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128)),
                ('demo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='physics.Demo')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributor', models.CharField(max_length=8)),
                ('text', models.CharField(max_length=2048)),
                ('demo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='physics.Demo')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200)),
                ('imagefile', models.ImageField(upload_to='photos/')),
                ('demo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='physics.Demo')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=8)),
            ],
        ),
        migrations.AddField(
            model_name='demo',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='physics.Room'),
        ),
    ]
