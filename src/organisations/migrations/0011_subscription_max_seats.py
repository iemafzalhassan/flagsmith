# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-12 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0010_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='max_seats',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]