    # -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
import datetime


class BookingForm(forms.Form):
    #Essential information for the Booking.
    initial_date = forms.DateField()
    final_date = forms.DateField()
