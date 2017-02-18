# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from cars.views import find_available_cars
from cars.models import Car
from booking.models import Dates_Reserved, Reservation
from .forms import SearchForm

import logging
import datetime



def index(request):
    # Check if the session has an error, based on last search.
    # If the error exists, use give it to the template and delete it from the session.
    if 'search_car_error_message' in request.session:
        message = request.session['search_car_error_message'].encode('utf8')
        print(message)
        context = {
            'error': True,
            'message': message
        }

        del request.session['search_car_error_message']


    else:
        context = {
            'error': False,
        }
    print(request.META['HTTP_HOST'])
    return render(request, 'frontpage/index.html', context)



def search_function(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            print('Valid search form, lets do some queries.')

            inital_date = search_form.cleaned_data['initial_date']
            final_date = search_form.cleaned_data['final_date']

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
                categories = categories.strip(", ")

            if not searched_types:
                searched_types = [1, 2, 3]
                categories = "Personbil, Varebil, Kombinertbil"

            # All cars of wanted Car Type
            filtered_cars = Car.objects.filter(car_type__in=searched_types)


            cars = find_available_cars(inital_date, final_date, filtered_cars)

            # The chosen dates did not find any cars. Redirect back to front with an error.
            if not cars:
                message = "Fant ingen ledige biler av kategori: %s i oppgitt periopde. Prøv igjen med ny kategori / periode, eller kontakt oss." % (categories)
                request.session['search_car_error_message'] = message

                return redirect(index)



            dates = {
                'initial_date': inital_date,
                'final_date': final_date
            }

            context = {
                'cars': cars,
                'initial_date': inital_date,
                'dates': dates,
                'categories': categories
            }
            return render(request, 'cars/car_list.html', context)

        else:
            print("mangler info i greia.")
            # TODO: Generate Error, same as booking input errors.
            message = "Informasjon mangler. Prøv å fyll ut begge dato feltene på nytt"
            request.session['search_car_error_message'] = message

            return redirect(index)
    else:
        return redirect('/')

