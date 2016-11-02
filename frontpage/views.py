# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from cars.models import Car
from booking.models import Dates_Reserved, Reservation
from .forms import SearchForm

import logging
import datetime



def index(request):

    """
    context = {
        'personal_cars': '',
        'van': '',
        'combi_car': '',
    }
    """

    if 'search_car_error_message' in request.session:
        message = request.session['search_car_error_message']
        print(message)
        context = {
            'error': True,
            'message': message
        }

    else:
        context = {
            'error': False,
        }
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
            cars = Car.objects.filter(car_type__in=searched_types)

            # All bookings of current cars
            car_bookings = Reservation.objects.filter(car__in=cars)


            # Overlapping by final date
            final_date_booking_overlap = car_bookings.filter(dates_reserved__final_date__range=(inital_date, final_date))
            # Overlapping by inital date
            initial_date_booking_overlap = car_bookings.filter(dates_reserved__initial_date__range=(inital_date, final_date))
            # Remove the cars with overlapping dates
            cars = cars.exclude(reserved_car__booking__car__in=final_date_booking_overlap.values("car")).exclude(reserved_car__booking__car__in=initial_date_booking_overlap.values("car"))


            # The chosen dates did not find any cars. Redirect back to front with an error.
            if not cars:
                message = "Fant ingen ledige biler av kategori: %s i oppgitt periopde. Prøv igjen med ny kategori / periode, eller kontakt oss." % (categories)
                request.session['search_car_error_message'] = message

                return redirect(index)

            print("There are cars!!")
            dates = {
                'initial_date': inital_date,
                'final_date': final_date
            }

            print(inital_date)
            context = {
                'cars': cars,
                'initial_date': inital_date,
                'dates': dates,
                'categories': categories
            }
            return render(request, 'cars/car_list.html', context)

        else:

            # TODO: Generate Error, same as booking input errors.
            message = "Informasjon mangler, prøv på nytt. <br> <p> Dato skal ha format: 'DD.MM.ÅÅÅÅ' </p>"
            search_error = True

            context = {
                'search_message_error': message,
                'search_error': search_error
            }
            return render(request, 'frontpage/index.html')

    else:
        return redirect('/')



def validate_date(initial_date, final_date):

    message = ""
    error = False

    if (final_date < initial_date):
        logging.info("Final date is before initial date")
        message = "Leveringsdagen er satt før Hente dagen, prøv på nytt."
        error = True


    # Less than 1 day searched, abort.
    if (final_date - initial_date).days < 1:
        logging.error("Less than 1 day, stop")
        message = "For liten leieperiode."
        error = True


    # User tries to search from before today, this is illegal.
    if initial_date < datetime.date.today():
        logging.error("Error, not able to search back in time.")
        message = "Kan ikke søke på dato tilbake i tid."
        error = True


    return True