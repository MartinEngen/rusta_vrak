# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import BookingForm, FilterForm
from .models import Car
from booking.models import Dates_Reserved, Reservation

from validation import validate_date, find_available_cars, validate_availability

import logging
import datetime

from booking.data_functions import generate_booked_dates


def car_list(request):
    if request.method == 'POST':
        # This method shall handle filtering of the objects AND searching for dates and availability.
        filtered_data = FilterForm(request.POST)
        if filtered_data.is_valid():
            # Initialize variables
            dates = False
            categories = ''
            searched_categories = ''
            car_types = []

            # Car type
            if filtered_data.cleaned_data['personal']:
                car_types.append(1)
                categories += 'Personbil, '
            if filtered_data.cleaned_data['van']:
                car_types.append(2)
                categories += 'Varebil, '
            if filtered_data.cleaned_data['combi_car']:
                car_types.append(3)
                categories += 'Kombinertbil, '

            if categories:
                categories = categories.strip(", ")

            if not car_types:
                car_types = [1, 2, 3]
                categories = 'Personbil, Varebil og Kombinertbil'

            # 0 is All seats
            seats = []
            # Specific number of seats
            if filtered_data.cleaned_data['seats'] > 0:
                seats.append(filtered_data.cleaned_data['seats'])
            else:
                # All seat combo's
                seats = [2, 3, 5, 7, 8, 9]


            transmission_types = []
            # Transmission
            if filtered_data.cleaned_data['transmission_auto']:
                transmission_types.append('Automatgir')
                searched_categories += 'Automat, '

            if filtered_data.cleaned_data['transmission_manual']:
                transmission_types.append('Manuell')
                searched_categories += 'Manuell, '

            if not transmission_types:
                transmission_types = ['Manuell', 'Automatgir']

            # Fuel
            fuel_types = []
            if filtered_data.cleaned_data['fuel_diesel']:
                fuel_types.append('Diesel')
                searched_categories += 'Diesel, '

            if filtered_data.cleaned_data['fuel_gasoline']:
                fuel_types.append('Bensin')
                searched_categories += 'Bensin, '

            if not fuel_types:
                fuel_types = ['Diesel', 'Bensin']

            cars = Car.objects.filter(car_type__in=car_types).filter(transmission__in=transmission_types).filter(fuel_type__in=fuel_types).filter(seats__in=seats).filter(for_rent=True)

            # Date Handler
            if filtered_data.cleaned_data['initial_date'] and filtered_data.cleaned_data['final_date']:
                initial_date = filtered_data.cleaned_data['initial_date']
                final_date = filtered_data.cleaned_data['final_date']

                validate = validate_date(initial_date, final_date)

                # If the validate does not return an error.
                if not validate['error']:
                    cars = find_available_cars(initial_date, final_date, cars)

                    dates = {
                        'initial_date': initial_date,
                        'final_date': final_date,
                    }

                else:
                    # User Entered non valid dates.
                    logging.error("Non Valid dates found, do redirect home. , %s" % validate['message'])
                    request.session['search_car_error_message'] = validate['message']

                    return redirect('/')

            context = {
                'cars': cars,
                'dates': dates,
                'categories': categories,
                'searched_categories': searched_categories
            }

            return render(request, 'cars/car_list.html', context)

        # Not valid POST request, redirect the user back to the start.
        else:
            logging.error("Invalid search form posted." + filtered_data.errors)
            request.session['search_car_error_message'] = "Feil oppstod ved henting av biler. Prøv igjen"

            return redirect('/')



    else:
        car_type = request.GET.get('type')

        if car_type:
            types = car_type.split(',')
            types = map(int, types)
        else:
            types = []

        # Initialize categories as an empty string.
        categories = ''
        if 1 in types:
            categories += 'Personbiler, '
        if 2 in types:
            categories += 'Varebiler, '
        if 3 in types:
            categories += 'Kombinertbiler, '

        # Remove the last comma and space.
        categories = categories.strip(", ")


        # IF not any type(s) given, show the user them all.
        if not types:
            types = [1, 2, 3]
            categories = 'Personbiler, Varebiler og Kombinertbiler'




        cars = Car.objects.filter(car_type__in=types).filter(for_rent=True)

        context = {
            'categories': categories,
            'cars': cars,
        }

        return render(request, 'cars/car_list.html', context)


def specific_car(request, car_id):

    # Standard Abort function.
    def abort_function(current_car, error_message, current_car_reservations):
        calendar_data = generate_booked_dates(current_car_reservations)
        context = {
            'car': current_car,
            'dates': 'false',
            'warning': True,
            'message': error_message,
            'booked_dates_json': calendar_data,
        }
        return render(request, 'cars/spesific_car.html', context)

    # POST Request
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        car = get_object_or_404(Car, id=car_id)

        if booking_form.is_valid():
            initial_date = booking_form.cleaned_data['initial_date']
            final_date = booking_form.cleaned_data['final_date']

            # Get all registered reservations for this car.
            existing_reservations = Reservation.objects.filter(car=car).exclude(final_date__lte=(datetime.date.today()))\
                .order_by('initial_date')

            # Run function to validate the two dates searched.
            validated_dates = validate_date(initial_date, final_date)
            if validated_dates['error']:
                return abort_function(car, validated_dates['message'], existing_reservations)

            # Checks the new dates against existing reservations and any reservation locks.
            validated_availability = validate_availability(initial_date, final_date, existing_reservations)
            if validated_availability['error']:
                return abort_function(car, validated_availability['message'], existing_reservations)

            # ============== Validation Passed ===============
            # Save the new record to the database.
            new_reservation = Dates_Reserved(car=car,
                                         initial_date=booking_form.cleaned_data['initial_date'],
                                         final_date=booking_form.cleaned_data['final_date']
                                         )
            new_reservation.save()
            request.session['current_booking_id'] = new_reservation.id
            return redirect('booking:reservation_schema', car_id=car.id)

        else:
            logging.debug("Non valid form posted.")
            existing_reservations = Reservation.objects.filter(car=car).exclude(
                final_date__lte=(datetime.date.today())) \
                .order_by('initial_date')
            message = "Informasjon mangler, prøv å fyll ut feltene på nytt. NB: Dato må være i format DD.MM.ÅÅÅÅ"

            return abort_function(car, message, existing_reservations)

    # GET request
    else:
        car = get_object_or_404(Car, id=car_id)

        images = image_generator(car)

        selected_dates = request.GET.values()

        if selected_dates:
            initial_date = selected_dates[1].encode('utf8')
            final_date = selected_dates[0].encode('utf8')

            dates = {
                'initial_date': initial_date,
                'final_date': final_date
            }
        else:
            dates = 'false'

        # Gather the information required by the Calendar
        existing_reservations = Reservation.objects.filter(car=car).exclude(
            final_date__lte=(datetime.date.today())) \
            .order_by('initial_date')

        booked_dates = generate_booked_dates(existing_reservations)

        context = {
            'car': car,
            'booked_dates_json': booked_dates,
            'images': images,
            'dates': dates
        }

        return render(request, 'cars/spesific_car.html', context)


def image_generator(car):
    """ Function to split up images for the gallery (if any)"""
    # Gallery images are stored as a string in the database
    # Simply split these strings by any ',' and store in a list.
    try:
        images_string = car.carimages.gallery_images.encode('utf-8')
    except ObjectDoesNotExist:
        return False

    # If the image string is not empty, split them up into a list.
    if images_string:
        images = images_string.split(',')
    else:
        images = False

    return images
