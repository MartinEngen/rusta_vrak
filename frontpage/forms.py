from django import forms


DATE_INPUT_FORMATS = [
    '%d.%m.%Y', # '12.02.2017'
    '%d/%m/%Y', #'12/02/2006'
]

class SearchForm(forms.Form):

    personal = forms.BooleanField(required=False)
    van = forms.BooleanField(required=False)
    combi_car = forms.BooleanField(required=False)

    initial_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    final_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)