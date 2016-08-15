# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-15 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20160815_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='extra',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='genre',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='links',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option4',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='pic_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]