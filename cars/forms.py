    # -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
import datetime




DATE_INPUT_FORMATS = [
    '%d.%m.%Y',  # '12.02.2017'
    '%d/%m/%Y',  # '12/02/2006'
]


class BookingForm(forms.Form):
    #Essential information for the Booking.
    initial_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    final_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)


class FilterForm(forms.Form):
    personal = forms.BooleanField(required=False)
    van = forms.BooleanField(required=False)
    combi_car = forms.BooleanField(required=False)

    seats = forms.IntegerField(max_value=12, required=False)


    transmission_manual = forms.BooleanField(required=False)
    transmission_auto = forms.BooleanField(required=False)

    fuel_gasoline = forms.BooleanField(required=False)
    fuel_diesel = forms.BooleanField(required=False)

    initial_date = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    final_date = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

