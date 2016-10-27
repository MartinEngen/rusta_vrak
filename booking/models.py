# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator
from django.db import models

from cars.models import Car

# Create your models here.
@python_2_unicode_compatible
class Car_Date_Reservation(models.Model):
    car = models.ForeignKey(Car, related_name='reserved_car', on_delete=models.CASCADE)

    initial_date = models.DateField('Hente Dato')
    final_date = models.DateField('Leverings Dato')

    status = models.PositiveSmallIntegerField('1: Pending, 2: Approved, 3:Declined', choices={(1, 'Pending'), (2, 'Approved'), (3, 'Declined')})

    def __str__(self):
        return str(self.id) + " " + self.car.brand + " " + self.car.model + ": Fra " + str(self.initial_date) + " Til: " + str(self.final_date)

    class Meta:
        verbose_name = 'dato_reservasjon'
        verbose_name_plural = 'dato_reservasjoner'




@python_2_unicode_compatible
class Registration_Schema(models.Model):
    car_date_reservation = models.ForeignKey(Car_Date_Reservation, related_name='booking', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='Bil', on_delete=models.CASCADE)

    # Information about the registrator
    first_name = models.CharField('Fornavn', max_length=100)
    last_name = models.CharField('Etternavn', max_length=100)

    email = models.EmailField('Epost adresse', max_length=100)
    phone_number = models.CharField('Telefonnummer', max_length=12, validators=[RegexValidator(r'^\d{1,10}$')])

    # Additional information
    misc_info = models.CharField('Ekstra informasjon', max_length=255, blank=True, null=True)

    date_made = models.DateField('Bestilligns dato', auto_now_add=True)


    def __str__(self):
        return self.car.brand + " " + self.car.model + ". " + str(self.date_made)


    class Meta:
        verbose_name = 'kontakt_skjema'
        verbose_name_plural = 'Ferdigstilte Bestillinger'
