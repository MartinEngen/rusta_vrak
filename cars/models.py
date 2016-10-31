# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator

from django.db import models

# Need to support python 2
@python_2_unicode_compatible
class Car(models.Model):

    #Misc information
    brand = models.CharField('Bilmerke', max_length=70)
    model = models.CharField('Biltype', max_length=70)
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    seats = models.PositiveSmallIntegerField('Antall seter')
    fuel_type = models.CharField('Type drivstoff', choices=[('Diesel', 'Diesel'), ('Bensin', 'Bensin'), ('Hybrid', 'Hybrid'), ('Elbil', 'Elbil')], max_length=20)

    main_image = models.CharField('Lenke til hovedbilde', max_length=50, default='')
    gallery_images = models.CharField('Bilder til galleri. Splitt lenkene via komma ","', max_length=255, blank=True, null=True)

    transmission = models.CharField('Gir', choices=[('Manuell', 'Manuell'), ('Automatgir', 'Automatgir')], default='Manuell', max_length=15)

    car_type = models.PositiveSmallIntegerField('Kategori', choices=[(1, 'Personbil'), (2, 'Varebil'), (3, 'Kombibil')])

    price = models.IntegerField('Dagspris leie', default=250)

    extra_accessories = models.CharField('Ekstra informasjon, splitt med komma (",")', blank=True, null=True, max_length=255)


    def __str__(self):
        return str(self.id) + " " + self.brand + " " + self.model

    class Meta:
        verbose_name = 'Bil'
        verbose_name_plural = 'Biler'