# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse


from django.shortcuts import get_object_or_404, redirect


from .forms import BookingForm

from .models import Car
from booking.models import Car_Date_Reservation, Registration_Schema

import logging
import datetime


from booking.data_functions import generate_calendar_data
from frontpage.views import index

# Mail API's
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Uniqueness
import hashlib

# TODO: Genereal Code Cleanup. This may entail moving some functions to new apps / files.

def car_list(request):
    car_type = request.GET.get('type')

    types = car_type.split(',')
    types = map(int, types)
    print(types)

    cars = Car.objects.filter(car_type__in=types)

    for car in cars:
        print (car.extra_accessories)
    context = {
        'cars': cars,
    }

    return render(request, 'cars/car_list.html', context)

def personal_car(request):
    personal_cars = Car.objects.filter(car_type=1)
    context = {
        'cars': personal_cars,
    }
    return render(request, 'cars/car_list.html', context)


def vans(request):
    vans = Car.objects.filter(car_type=2)
    context = {
        'cars': vans,
    }
    return render(request, 'cars/car_list.html', context)

def combi_car(request):
    combi_car = Car.objects.filter(car_type=3)
    context = {
        'cars': vans,
    }
    return render(request, 'cars/car_list.html', context)

def specific_car(request, car_id):

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
            #car_bookings = Car_Booking.objects.filter(car=car).exclude(final_date__lte=datetime.date.today()).order_by(
            #    'initial_date')

            finalized_bookings = Registration_Schema.objects.filter(car=car).exclude(
                car__reserved_car__final_date__lte=datetime.date.today()).order_by('car_date_reservation__initial_date')


            if(final_date<initial_date):
                logging.info("Final date is before initial date")
                print("Abort, now..")
                message = "Leveringsdagen er satt før 'Hente' dagen, prøv på nytt."
                calendar_data = generate_calendar_data(finalized_bookings)

                context = {
                    'car': car,
                    # 'bookings': car_bookings,
                    'warning': True,
                    'message': message,
                    'json_data_string': calendar_data,
                }

                return render(request, 'cars/spesific_car.html', context)



            if(final_date - initial_date).days < 1:
                logging.error("Less than 1 day, stop")
                message = "For liten leieperiode."

                calendar_data = generate_calendar_data(finalized_bookings)

                context = {
                    'car': car,
                    # 'bookings': car_bookings,
                    'warning': True,
                    'message': message,
                    'json_data_string': calendar_data,
                }

                #return render(request, 'cars/spesific_car.html', context)




            if (final_date - initial_date).days > 30:
                logging.error("Logging more than 30 days, Stop.")
                message = "Kan ikke reservere mer enn 30 dager i gangen. Ta kontakt for en større reservasjon."

                calendar_data = generate_calendar_data(finalized_bookings)

                context = {
                    'car': car,
                    #'bookings': car_bookings,
                    'warning': True,
                    'message': message,
                    'json_data_string': calendar_data,
                }

                return render(request, 'cars/spesific_car.html', context)

            # User tries to book from before today, this is illegal.
            if initial_date < datetime.date.today():
                logging.error("Error, not able to book.")
                message = "Kan ikke registerer en reservasjon som går tilbake i tid."

                calendar_data = generate_calendar_data(finalized_bookings)

                context = {
                    'car': car,
                    #'bookings': car_bookings,
                    'warning': True,
                    'message': message,
                    'json_data_string': calendar_data,
                }

                return render(request, 'cars/spesific_car.html', context)

            # Check if the dates are valid, this means that all the dates inbetween are also not already booked.
            # TODO: Change to look at the finalized bookings, not the halfass ones.
            for finalized_booking in finalized_bookings:
                if finalized_booking.car_date_reservation.initial_date <= initial_date and finalized_booking.car_date_reservation.final_date >= initial_date or finalized_booking.car_date_reservation.initial_date <= final_date and finalized_booking.car_date_reservation.final_date >= final_date:
                    logging.error("Error, not able to book.")
                    message = "Reservasjon overlapper, velg en ledig periode."

                    calendar_data = generate_calendar_data(finalized_bookings)

                    context = {
                        'car': car,
                        # 'bookings': car_bookings,
                        'warning': True,
                        'message': message,
                        'json_data_string': calendar_data,
                    }

                    return render(request, 'cars/spesific_car.html', context)

            new_booking = Car_Date_Reservation(car=car, initial_date=booking_form.cleaned_data['initial_date'],
                                      final_date=booking_form.cleaned_data['final_date'], status=2)
            new_booking.save()
            return redirect('booking:reservation_schema', booking_id=new_booking.id, car_id=car.id)


        else:

            print("Not Valid.")
            logging.debug("Non valid form posted.")
            print(booking_form.errors)

            finalized_bookings = Registration_Schema.objects.filter(car=car).exclude(
                car__reserved_car__final_date__lte=datetime.date.today()).order_by('car_date_reservation__initial_date')
            calendar_data = generate_calendar_data(finalized_bookings)
            message = "Mangler Informasjon, prøv igjen."
            context = {
                'car': car,
                'warning': True,
                'message': message,
                'json_data_string': calendar_data,
            }

            return render(request, 'cars/spesific_car.html',context)

    else:
        current_car = get_object_or_404(Car, id=car_id)

        images_string = current_car.gallery_images.encode('utf-8')


        if images_string:
            print(images_string)
            images = images_string.split(',')
        else:
            images = False


        # Gather the information required by the Calendar
        finalized_bookings = Registration_Schema.objects.filter(car=current_car).exclude(
            car__reserved_car__final_date__lte=datetime.date.today()).order_by('car__reserved_car__initial_date')

        calendar_data = generate_calendar_data(finalized_bookings)

        context = {
            'car': current_car,
            #'bookings': car_bookings,
            'json_data_string': calendar_data,
            'bilder': images
        }

        return render(request, 'cars/spesific_car.html', context)



def booking_receipt(request, booking_id, registration_id):
    # TODO: Get the information required for the receipt page. Send this to the view and display it.



    return render(request, 'booking/booking_receipt.html')
