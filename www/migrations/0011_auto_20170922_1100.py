# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0010_country_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adPlace', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='www.AdPlace')),
                ('adType', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='www.AdType')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='www.ApplicationAdConfig')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='www.Platform')),
            ],
        ),
        migrations.AddField(
            model_name='applicationad',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='www.ApplicationPlatform'),
        ),
        migrations.AlterUniqueTogether(
            name='applicationplatform',
            unique_together=set([('config', 'platform')]),
        ),
        migrations.AlterUniqueTogether(
            name='applicationad',
            unique_together=set([('platform', 'adType', 'adPlace')]),
        ),
    ]
