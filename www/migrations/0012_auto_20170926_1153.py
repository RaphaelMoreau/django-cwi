# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0011_auto_20170922_1100'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApplicationAdConfig',
            new_name='ApplicationCountry',
        ),
    ]
