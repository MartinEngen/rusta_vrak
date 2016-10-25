    # -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
import datetime


class BookingForm(forms.Form):
    #Essential information for the Booking.
    initial_date = forms.DateField()
    final_date = forms.DateField()



class BookingRegistrationForm(forms.Form):
    first_name = forms.CharField(label='Fornavn', max_length=100)
    last_name = forms.CharField(label='Etternavn', max_length=100)

    email = forms.EmailField(label='Epost adresse', max_length=100)
    phone_number = forms.CharField(max_length=12)#, validators=[RegexValidator(r'^\d{1,10}$')]

    misc_info = forms.CharField(label='Ekstra informasjon (Maks 255 Karakterer)', max_length=255, required=False)
