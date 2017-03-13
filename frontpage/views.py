# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

from cars.views import find_available_cars
from cars.models import Car
from .forms import SearchForm



def index(request):
    # Check if the session (for this user) has any errors.
    # If the error exists, use give it to the template and delete the processed error from the session.
    if 'search_car_error_message' in request.session:
        message = request.session['search_car_error_message'].encode('utf8')
        context = {
            'error': True,
            'message': message
        }
        del request.session['search_car_error_message']

    else:
        # Telling the Template that there is no error.
        context = {
            'error': False,
        }


    return render(request, 'frontpage/index.html', context)


# Searching to find any available cars between two given dates.
def search_function(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            initial_date = search_form.cleaned_data['initial_date']
            final_date = search_form.cleaned_data['final_date']


            # Any extra requirements handleded.
            searched_types = []
            categories = ''
            if search_form.cleaned_data['personal']:
                searched_types.append(1)
                categories += 'Personbil, '
            if search_form.cleaned_data['van']:
                searched_types.append(2)
                categories += 'Varebil, '
            if search_form.cleaned_data['combi_car']:
                searched_types.append(3)
                categories += 'Kombinertbil, '

            if categories:
                # Remove the trailing ', ' from the string.
                # This is the string shown to the user of which categories used in the search.
                categories = categories.strip(", ")

            # No type categories specified.
            if not searched_types:
                searched_types = [1, 2, 3]
                categories = "Personbil, Varebil, Kombinertbil"

            # All cars of wanted Car Type
            filtered_cars = Car.objects.filter(car_type__in=searched_types)

            # Available cars.
            cars = find_available_cars(initial_date, final_date, filtered_cars)

            # The chosen dates did not find any cars. Redirect back to front with an error.
            if not cars:
                message = "Fant ingen ledige biler av kategori: %s i oppgitt periopde. Prøv igjen med ny kategori / periode, eller kontakt oss." % (categories)
                request.session['search_car_error_message'] = message

                return redirect(index)



            dates = {
                'initial_date': initial_date,
                'final_date': final_date
            }

            context = {
                'cars': cars,
                'initial_date': initial_date,
                'dates': dates,
                'categories': categories
            }
            return render(request, 'cars/car_list.html', context)

        # Non Valid form posted. Returns a general 'Information Missing, try again' error.
        else:
            message = "Informasjon mangler. Prøv å fyll ut begge dato feltene på nytt"
            request.session['search_car_error_message'] = message
            return redirect(index)

    # GET request, might not be necessary, consider removing.
    # TODO: Figure out if GET requests are possible in POST functions.
    else:
        return redirect('/')

