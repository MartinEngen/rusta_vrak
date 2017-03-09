    # -*- coding: utf-8 -*-
from django import forms
import datetime



DATE_INPUT_FORMATS = [
    '%d.%m.%Y', # '12.02.2017'
    '%d/%m/%Y', #'12/02/2006'
]


class LockReservationsForm(forms.Form):
    #Essential information for the Booking.
    from_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    to_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
