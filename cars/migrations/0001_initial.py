# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=70, verbose_name='Bilmerke')),
                ('model', models.CharField(max_length=70, verbose_name='Biltype')),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('seats', models.PositiveSmallIntegerField(verbose_name='Antall seter')),
                ('fuel_type', models.CharField(choices=[('Diesel', 'Diesel'), ('Bensin', 'Bensin'), ('Hybrid', 'Hybrid'), ('Elbil', 'Elbil')], max_length=20, verbose_name='Type drivstoff')),
                ('main_image', models.CharField(default='', max_length=50, verbose_name='Lenke til hovedbilde')),
                ('gallery_images', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilder til galleri. Splitt lenkene via komma ","')),
                ('transmission', models.CharField(choices=[('Manuell', 'Manuell'), ('Automatgir', 'Automatgir')], default='Manuell', max_length=15, verbose_name='Gir')),
                ('car_type', models.PositiveSmallIntegerField(choices=[(1, 'Personbil'), (2, 'Varebil'), (3, 'Kombibil')], verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Bil',
                'verbose_name_plural': 'Biler',
            },
        ),
    ]
