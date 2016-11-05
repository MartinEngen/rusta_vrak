    # -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
import datetime


class BookingForm(forms.Form):
    #Essential information for the Booking.
    initial_date = forms.DateField()
    final_date = forms.DateField()



class FilterForm(forms.Form):
    personal = forms.BooleanField(required=False)
    van = forms.BooleanField(required=False)
    combi_car = forms.BooleanField(required=False)

    seats = forms.IntegerField(max_value=12, required=False)


    transmission_manual = forms.BooleanField(required=False)
    transmission_auto = forms.BooleanField(required=False)

    fuel_gasoline = forms.BooleanField(required=False)
    fuel_diesel = forms.BooleanField(required=False)
