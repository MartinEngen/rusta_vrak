# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, redirect


from .forms import BookingForm, FilterForm
from .models import Car
from booking.models import Dates_Reserved, Reservation

import logging
import datetime

from booking.data_functions import generate_calendar_data
from frontpage.views import index

# Mail API's
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO: Genereal Code Cleanup. This may entail moving some functions to new apps / files.

def car_list(request):
    # TODO: Make the search queries based on posted from the car_list page
    if request.method == 'POST':

        filtered_data = FilterForm(request.POST)

        if filtered_data.is_valid():
            print(filtered_data)

            car_types = []
            # Car type
            if filtered_data.cleaned_data['personal']:
                car_types.append(1)


            if filtered_data.cleaned_data['van']:
                car_types.append(2)


            if filtered_data.cleaned_data['combi_car']:
                car_types.append(3)

            if not car_types:
                car_types = [1, 2, 3]

            print(car_types)

            # 0 is All seats
            seats = []
            #Spesific number of seats
            if filtered_data.cleaned_data['seats'] > 0:
                #seats = filtered_data.cleaned_data['seats']
                seats.append(filtered_data.cleaned_data['seats'])
            else:
                # All seat combo's
                seats = [1,2,3,4,5,6,7,8,9,10,11,12]

            print(seats)

            transmission_types = []
            # Transmission
            if filtered_data.cleaned_data['transmission_auto']:
                transmission_types.append('Automatgir')

            if filtered_data.cleaned_data['transmission_manual']:
                transmission_types.append('Manuell')


            if not transmission_types:
                transmission_types = ['Manuell', 'Automatgir']

            print(filtered_data.cleaned_data['transmission_auto'])
            print(transmission_types)

            # Fuel
            fuel_types = []
            if filtered_data.cleaned_data['fuel_diesel']:
                fuel_types.append('Diesel')
                pass
            if filtered_data.cleaned_data['fuel_gasoline']:
                fuel_types.append('Bensin')
                pass


            if not fuel_types:
                fuel_types = ['Diesel', 'Bensin']



            print(fuel_types)
            cars = Car.objects.filter(car_type__in=car_types).filter(transmission__in=transmission_types).filter(fuel_type__in=fuel_types).filter(seats__in=seats)

            print("Valid ")
            context = {
                'cars': cars
            }
            return render(request, 'cars/car_list.html', context)
            #return redirect('/')



        # Not valid POST request, redirect the user back to the start.
        else:
            return redirect('/')



    else:

        car_type = request.GET.get('type')

        if car_type:
            types = car_type.split(',')
            types = map(int, types)
        else:
            types = []


        categories = ''
        if 1 in types:
            categories += 'Personbiler, '
        if 2 in types:
            categories += 'Varebiler, '
        if 3 in types:
            categories += 'Kombinertbiler, '

        categories = categories.strip(", ")


        # IF not any type(s) given, show the user them all.
        if not types:
            types = [1, 2, 3]
            categories = 'Personbiler, Varebiler og Kombinertbiler'




        cars = Car.objects.filter(car_type__in=types)

        for car in cars:
            print (car.extra_accessories)
        context = {
            'categories': categories,
            'cars': cars,
        }

        return render(request, 'cars/car_list.html', context)



# Validate dates before reservation.
def validate_date(initial_date, final_date):

    message = ''
    error = False


      # Less than 1 day booked, abort.
    if (final_date - initial_date).days < 1:
        logging.error("Less than 1 day, stop")
        message = "For liten leieperiode."
        error = True


    # Final date before the inital date.
    if (final_date < initial_date):
        logging.info("Final date is before initial date")
        message = "Leveringsdagen er satt før Hente dagen, gjør om og prøv på nytt."
        error = True
        # calendar_data = generate_calendar_data(finalized_bookings)


        # More than 30 days booked, abort.
    if (final_date - initial_date).days > 30:
        logging.error("Logging more than 30 days, Stop.")
        message = "Kan ikke reservere mer enn 30 dager i gangen. Ta kontakt for en større reservasjon."
        error = True


        # User tries to book from before today, this is illegal.
    if initial_date < datetime.date.today():
        logging.error("Error, not able to book.")
        message = "Kan ikke registerer en reservasjon tilbake i tid."
        error = True


    context = {
        'message': message,
        'error': error
    }

    return context


def specific_car(request, car_id):

    def abort_function(car, message, finalized_bookings):
        calendar_data = generate_calendar_data(finalized_bookings)
        print("Calendar data ERROR size: " + str(finalized_bookings.count()))
        context = {
            'car': car,
            # 'bookings': car_bookings,
            'dates': 'false',
            'warning': True,
            'message': message,
            'json_data_string': calendar_data,
        }
        return render(request, 'cars/spesific_car.html', context)



    # POST Request
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)

        # logging.info("Booking Requested.")
        print ("Booking Requested.")
        car = get_object_or_404(Car, id=car_id)
        if booking_form.is_valid():

            initial_date = booking_form.cleaned_data['initial_date']
            final_date = booking_form.cleaned_data['final_date']

            # Check if the number of days exeeds 30 days.
            # Get all registered bookings for this car.
            finalized_bookings = Reservation.objects.filter(car=car).exclude(dates_reserved__final_date__lte=(datetime.date.today()))\
                .order_by('dates_reserved__initial_date')



            # Run function to validate the dates searched.
            validated_dates = validate_date(initial_date, final_date)

            if validated_dates['error']:
                return abort_function(car, validated_dates['message'], finalized_bookings)



            # Check if the dates are valid, this means that all the dates inbetween are also not already booked.
            for finalized_booking in finalized_bookings:


                # Checks if the date is placed within a range of already booked.
                if finalized_booking.dates_reserved.initial_date <= initial_date <= finalized_booking.dates_reserved.final_date or finalized_booking.dates_reserved.initial_date <= final_date <= finalized_booking.dates_reserved.final_date:
                    print("Complicated working..")
                    logging.error("Error, not able to book. Overlapping")
                    message = "Reservasjon overlapper, velg en ledig periode."
                    return abort_function(car, message, finalized_bookings)


                # Check if there is an exisiting booking within this new entry.
                if initial_date <= finalized_booking.dates_reserved.initial_date <= final_date or initial_date <= finalized_booking.dates_reserved.final_date <= final_date:
                    print("Complicated working..")
                    logging.error("Error, not able to book. Overlapping")
                    message = "Reservasjon overlapper, velg en ledig periode."
                    return abort_function(car, message, finalized_bookings)




                """
                if (finalized_booking.dates_reserved.initial_date <= initial_date and finalized_booking.dates_reserved.final_date >= initial_date) or (finalized_booking.dates_reserved.initial_date <= final_date and finalized_booking.dates_reserved.final_date >= final_date):
                    print("Complicated working..")
                    logging.error("Error, not able to book. Overlapping")
                    message = "Reservasjon overlapper, velg en ledig periode."
                    return abort_function(car, message, finalized_bookings)
                """


            new_booking = Dates_Reserved(car=car, initial_date=booking_form.cleaned_data['initial_date'],
                                      final_date=booking_form.cleaned_data['final_date'])
            new_booking.save()


            request.session['current_booking_id'] = new_booking.id
            return redirect('booking:reservation_schema', car_id=car.id)


        else:

            print("Not Valid.")
            logging.debug("Non valid form posted.")
            print(booking_form.errors)
            #car = get_object_or_404(Car, id=car_id)
            finalized_bookings = Reservation.objects.filter(car=car).exclude(
                dates_reserved__final_date__lte=(datetime.date.today())) \
                .order_by('dates_reserved__initial_date')

            message = "Informasjon mangler, prøv å fyll ut feltene på nytt. Dato må være DD.MM.ÅÅÅÅ"

            return abort_function(car, message, finalized_bookings)


    # GET request
    else:
        current_car = get_object_or_404(Car, id=car_id)

        images_string = current_car.gallery_images.encode('utf-8')
        images = images_string.split(',')

        images = image_generator(current_car)



        from_date = request.GET.values()

        if from_date:
            initial_date = from_date[1].encode('utf8')
            final_date = from_date[0].encode('utf8')

            # This is the one I need.
            print(initial_date)
            print(final_date)
            dates = {
                'initial_date': initial_date,
                'final_date': final_date
            }
        else:
            dates = 'false'


        print(from_date)

        # Gather the information required by the Calendar
        #finalized_bookings = Reservation.objects.filter(car=current_car).exclude(dates_reserved__final_date__lte=datetime.datetime.today()).order_by('car__reserved_car__initial_date')
        finalized_bookings = Reservation.objects.filter(car=current_car).exclude(
            dates_reserved__final_date__lte=(datetime.date.today())) \
            .order_by('dates_reserved__initial_date')

        print("GET bookings: " + str(finalized_bookings.count()))
        print(finalized_bookings)
        calendar_data = generate_calendar_data(finalized_bookings)
        #print("Calendar data GET size: " + str(finalized_bookings.count()))

        context = {
            'car': current_car,
            'json_data_string': calendar_data,
            'images': images,
            'dates': dates
        }

        return render(request, 'cars/spesific_car.html', context)


def image_generator(car):
    images_string = car.gallery_images.encode('utf-8')

    # If the image string is not empty, split them up into a list.
    if images_string:
        images = images_string.split(',')

    else:
        images = False

    return images







def booking_receipt(request, booking_id, registration_id):
    # TODO: Get the information required for the receipt page. Send this to the view and display it.



    return render(request, 'booking/booking_receipt.html')
