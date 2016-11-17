# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-17 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_car_license_plate'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='for_rent',
            field=models.BooleanField(default=True, verbose_name='Bilen klar for utleie.'),
        ),
    ]
