# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-05 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170205_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(default='BadCourseName', max_length=96),
            preserve_default=False,
        ),
    ]
