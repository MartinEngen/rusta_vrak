# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-31 15:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_auto_20161019_1336'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False, verbose_name='Epost Adresse')),
                ('first_name', models.CharField(max_length=100, verbose_name='Fornavn')),
                ('last_name', models.CharField(max_length=100, verbose_name='Etternavn')),
                ('num_orders', models.IntegerField(default=0, verbose_name='Antall bestilinger')),
                ('phone_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')], verbose_name='Telefonnummer')),
            ],
            options={
                'verbose_name': 'Kunde',
                'verbose_name_plural': 'Kunder',
            },
        ),
        migrations.CreateModel(
            name='Dates_Reserved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_date', models.DateField(verbose_name='Hente Dato')),
                ('final_date', models.DateField(verbose_name='Leverings Dato')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_car', to='cars.Car')),
            ],
            options={
                'verbose_name': 'dato_reservasjon',
                'verbose_name_plural': 'dato_reservasjoner',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('misc_info', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ekstra informasjon')),
                ('status', models.PositiveSmallIntegerField(choices=[(2, 'Approved'), (1, 'Pending'), (3, 'Declined')], verbose_name='1: Pending, 2: Approved, 3:Declined')),
                ('date_made', models.DateField(auto_now_add=True, verbose_name='Bestilligns dato')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bil', to='cars.Car')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Kunde', to='booking.Customer')),
                ('dates_reserved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='booking.Dates_Reserved')),
            ],
            options={
                'verbose_name': 'kontakt_skjema',
                'verbose_name_plural': 'Ferdigstilte Bestillinger',
            },
        ),
        migrations.RemoveField(
            model_name='car_date_reservation',
            name='car',
        ),
        migrations.RemoveField(
            model_name='registration_schema',
            name='car',
        ),
        migrations.RemoveField(
            model_name='registration_schema',
            name='car_date_reservation',
        ),
        migrations.DeleteModel(
            name='Car_Date_Reservation',
        ),
        migrations.DeleteModel(
            name='Registration_Schema',
        ),
    ]
