# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0005_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='code',
        ),
        migrations.AddField(
            model_name='country',
            name='codeA2',
            field=models.CharField(default=None, max_length=2, primary_key=True, serialize=False, verbose_name='ISO Alpha2 code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='codeA3',
            field=models.CharField(default=None, max_length=3, verbose_name='ISO Alpha3 code'),
            preserve_default=False,
        ),
    ]