# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-05 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textbook',
            name='author',
            field=models.CharField(max_length=96),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='sku',
            field=models.CharField(max_length=96),
        ),
    ]
