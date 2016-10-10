from django import forms

class SearchForm(forms.Form):

    personal = forms.BooleanField(required=False)
    van = forms.BooleanField(required=False)
    combi_car = forms.BooleanField(required=False)

    initial_date = forms.DateField()
    final_date = forms.DateField()