# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 10:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0012_auto_20170926_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationplatform',
            old_name='config',
            new_name='country',
        ),
        migrations.AlterUniqueTogether(
            name='applicationplatform',
            unique_together=set([('country', 'platform')]),
        ),
    ]