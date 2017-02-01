# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailverification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='id',
        ),
        migrations.AlterField(
            model_name='email',
            name='email_id',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
    ]
