# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator
from django.db import models

from cars.models import Car

# Create your models here.
@python_2_unicode_compatible
class Dates_Reserved(models.Model):
    car = models.ForeignKey(Car, related_name='reserved_car', on_delete=models.CASCADE)

    initial_date = models.DateField('Hente Dato')
    final_date = models.DateField('Leverings Dato')

    def __str__(self):
        return str(self.id) + " " + self.car.brand + " " + self.car.model + ": Fra " + str(self.initial_date) + " Til: " + str(self.final_date)

    class Meta:
        verbose_name = 'dato_reservasjon'
        verbose_name_plural = 'dato_reservasjoner'


@python_2_unicode_compatible
class Customer(models.Model):
    email = models.EmailField('Epost Adresse', primary_key=True, max_length=100)

    #Customer Information
    first_name = models.CharField('Fornavn', max_length=100)
    last_name = models.CharField('Etternavn', max_length=100)

    num_orders = models.IntegerField('Antall bestilinger', default=0)

    phone_number = models.CharField('Telefonnummer', max_length=12, validators=[RegexValidator(r'^\d{1,10}$')])


    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Kunde'
        verbose_name_plural = 'Kunder'


@python_2_unicode_compatible
class Reservation(models.Model):
    #dates_reserved = models.ForeignKey(Dates_Reserved, related_name='booking', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='Bil', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='Kunde', on_delete=models.CASCADE)

    # Additional information
    misc_info = models.CharField('Ekstra informasjon', max_length=255, blank=True, null=True)

    # Reservation Status
    status = models.PositiveSmallIntegerField('1: Pending, 2: Approved, 3:Declined',
                                              choices={(1, 'Pending'), (2, 'Approved'), (3, 'Declined')})

    initial_date = models.DateField('Hente Dato')
    final_date = models.DateField('Leverings Dato')

    date_made = models.DateField('Bestilligns dato', auto_now_add=True)


    def __str__(self):
        return self.car.brand + " " + self.car.model + ". " + str(self.date_made)


    class Meta:
        verbose_name = 'Reservasjon'
        verbose_name_plural = 'Fullførte Bestillinger'