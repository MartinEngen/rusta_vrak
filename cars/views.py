# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import BookingForm, FilterForm
from .models import Car, CarImages
from booking.models import Dates_Reserved, Reservation
from control_panel.models import lock_reservation_period

from validation_functions import validate_date, find_available_cars

import logging
import datetime

from booking.data_functions import generate_booked_dates

# Mail API's
# TODO: General Code Cleanup. This may entail moving some functions to new apps / files.

def car_list(request):
    # TODO: Make the search queries based on posted from the car_list page
    if request.method == 'POST':
        # This method shall handle filtering of the objects AND searching for dates and availability.
        filtered_data = FilterForm(request.POST)




        if filtered_data.is_valid():
            # Initialze variables
            dates = False
            categories = ''
            searched_categories = ''
            validate = {
                'error': False
            }

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
            #Spesific number of seats
            if filtered_data.cleaned_data['seats'] > 0:
                #seats = filtered_data.cleaned_data['seats']
                seats.append(filtered_data.cleaned_data['seats'])
            else:
                # All seat combo's
                seats = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


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

            # No Cars has been found on the given terms.
            if not cars:
                # TODO: Redirect and popup when this happens.
                pass

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
    def abort_function(car, message, finalized_bookings):
        calendar_data = generate_booked_dates(finalized_bookings)
        context = {
            'car': car,
            'dates': 'false',
            'warning': True,
            'message': message,
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

            # Get all registered bookings for this car.
            finalized_bookings = Reservation.objects.filter(car=car).exclude(final_date__lte=(datetime.date.today()))\
                .order_by('initial_date')

            # Run function to validate the dates searched.
            validated_dates = validate_date(initial_date, final_date)

            if validated_dates['error']:
                return abort_function(car, validated_dates['message'], finalized_bookings)


            # All locked periods.
            existing_reservation_locks = lock_reservation_period.objects.filter(to_date__gte=datetime.date.today())

            # Check if the dates are valid, this means that all the dates inbetween are also not already booked.
            for finalized_booking in finalized_bookings:

                # Checks if the date is placed within a range of already booked.
                if finalized_booking.initial_date <= initial_date <= finalized_booking.final_date or finalized_booking.initial_date <= final_date <= finalized_booking.final_date:
                    logging.error("Error, not able to book. Overlapping")
                    message = "Reservasjon overlapper, velg en ledig periode."
                    return abort_function(car, message, finalized_bookings)

                # Check if there is an exisiting booking within this new entry.
                if initial_date <= finalized_booking.initial_date <= final_date or initial_date <= finalized_booking.final_date <= final_date:
                    logging.error("Error, not able to book. Overlapping")
                    message = "Reservasjon overlapper, velg en ledig periode."
                    return abort_function(car, message, finalized_bookings)

                # TODO: Add check for no business dates.
            




            new_booking = Dates_Reserved(car=car, initial_date=booking_form.cleaned_data['initial_date'],
                                      final_date=booking_form.cleaned_data['final_date'])
            new_booking.save()

            request.session['current_booking_id'] = new_booking.id


            return redirect('booking:reservation_schema', car_id=car.id)


        else:
            logging.debug("Non valid form posted.")
            finalized_bookings = Reservation.objects.filter(car=car).exclude(
                final_date__lte=(datetime.date.today())) \
                .order_by('initial_date')

            message = "Informasjon mangler, prøv å fyll ut feltene på nytt. Dato må være DD.MM.ÅÅÅÅ"

            return abort_function(car, message, finalized_bookings)


    # GET request
    else:
        current_car = get_object_or_404(Car, id=car_id)


        images = image_generator(current_car)



        from_date = request.GET.values()

        if from_date:
            initial_date = from_date[1].encode('utf8')
            final_date = from_date[0].encode('utf8')

            dates = {
                'initial_date': initial_date,
                'final_date': final_date
            }
        else:
            dates = 'false'
        # Gather the information required by the Calendar
        #finalized_bookings = Reservation.objects.filter(car=current_car).exclude(dates_reserved__final_date__lte=datetime.datetime.today()).order_by('car__reserved_car__initial_date')
        finalized_bookings = Reservation.objects.filter(car=current_car).exclude(
            final_date__lte=(datetime.date.today())) \
            .order_by('initial_date')

        booked_dates = generate_booked_dates(finalized_bookings)
        #print("Calendar data GET size: " + str(finalized_bookings.count()))

        context = {
            'car': current_car,
            'booked_dates_json': booked_dates,
            'images': images,
            'dates': dates
        }

        return render(request, 'cars/spesific_car.html', context)











def image_generator(car):
    try:
        images_string = car.carimages.gallery_images.encode('utf-8')
    except ObjectDoesNotExist:
        images = False
        return images



    # If the image string is not empty, split them up into a list.
    if images_string:
        images = images_string.split(',')
    else:
        images = False

    return images
