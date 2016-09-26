# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

# Create your views here.
from django.shortcuts import get_object_or_404, redirect


from .forms import BookingForm, BookingRegistrationForm

from .models import Car, Car_Booking, Registration_Scheme
import logging
import datetime
import json
from django.core import serializers
from django.http import JsonResponse

from frontpage.views import index

import smtplib
import os


def personal_car(request):


    personal_cars = Car.objects.filter(car_type=1)


    context = {
        'personal_cars': personal_cars,
    }

    return render(request, 'cars/personal_cars.html', context)





def car_availability(request, car_id):

    if request.method == 'POST':

        booking_form = BookingForm(request.POST)
        #logging.info("Booking Requested.")
        print ("Booking Requested.")
        car = get_object_or_404(Car, id=car_id)
        if booking_form.is_valid():
            print("Valid")

            initial_date = booking_form.cleaned_data['initial_date']
            final_date = booking_form.cleaned_data['final_date']

            # User tries to book from before today, this is illegal.
            if(initial_date < datetime.date.today()):
                print("Before today. Or TOday")



            # Check if the dates are valid, this means that all the dates inbetween are also not already booked.

            # Get all registered bookings for this car.
            car_bookings = Car_Booking.objects.filter(car=car).exclude(final_date__lte=datetime.date.today())
            for booking in car_bookings:
                if (booking.initial_date <= initial_date and booking.final_date >= initial_date) or (booking.initial_date <= final_date and booking.final_date >= final_date):
                    print ("Error, not able to book")
                    logging.info("Error, not able to book.")
                    warning = True
                    message = "Overlapping av booking detektert."
                    return render(request, 'cars/spesific_car.html', {'car': car, 'bookings': car_bookings, 'warning': warning, 'message': message})


            new_booking = Car_Booking(car=car, initial_date=booking_form.cleaned_data['initial_date'], final_date=booking_form.cleaned_data['final_date'], status=2)
            new_booking.save()

            return redirect('cars:booking_scheme', booking_id=new_booking.id, car_id=car.id)






            #return redirect(booking_schema(request, new_booking, car))
            #new_booking.save()




        else:
            print("Not Valid.")
            logging.debug("Non valid form posted.")
            print(booking_form.errors)

        car_bookings = Car_Booking.objects.filter(car=car)


        return render(request, 'cars/spesific_car.html', {'car': car, 'bookings': car_bookings,})

    else:

        current_car = get_object_or_404(Car, id=car_id)
        car_bookings = Car_Booking.objects.filter(car=current_car).exclude(final_date__lte=datetime.date.today()).order_by('initial_date')

        imagesString = current_car.gallery_images

        images = imagesString.split(',')


        data = []

        for booking in car_bookings:
            start_date = booking.initial_date
            end_date = booking.final_date

            event = {'start': str(start_date), 'end': str(end_date + datetime.timedelta(days=1)), 'rendering': 'background', 'color': 'black'}
            data.append(event)


        json_data_string = json.dumps(data)


        context = {
            'car': current_car,
            'bookings': car_bookings,
            'json_data_string': json_data_string,
            'bilder': images
        }

        return render(request, 'cars/spesific_car.html', context)


def booking_schema(request, booking_id, car_id):

    if request.method == 'POST':

        booking_scheme_form = BookingRegistrationForm(request.POST)

        if booking_scheme_form.is_valid():
            print("Valid")
            first_name = booking_scheme_form.cleaned_data['first_name']
            last_name = booking_scheme_form.cleaned_data['last_name']

            email = booking_scheme_form.cleaned_data['email']
            phone_number = booking_scheme_form.cleaned_data['phone_number']
            misc_info = booking_scheme_form.cleaned_data['misc_info']

            current_car = get_object_or_404(Car, id=car_id)
            current_booking = get_object_or_404(Car_Booking, id=booking_id)

            new_form = Registration_Scheme(car_id=car_id, booking_id=booking_id,
                                           email=email, phone_number=phone_number, first_name=first_name,
                                           last_name=last_name, misc_info=misc_info)
            new_form.save()

            if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
                from google.appengine.api import mail

                mail.send_mail(sender='Nitrax92@gmail.com',
                               to="%s %s <%s>" % (new_form.first_name, new_form.last_name, new_form.email),
                               subject="Kvittering. Rusta Vrak Bilutleige",
                               body="""Hei %s,
                Her kommer en kvittering.
                Bookingnummer: %s.
                Fra Dato: %s
                Til Dato: %s
                Pris: %s ,-


                Epost: rusta.vrak@gmail.com
                Telefon +47 400 49 489
                """ % (new_form.first_name, str(booking_id), str(current_booking.initial_date.strftime('%d-%m-%Y')), str(current_booking.final_date.strftime('%Y-%m-%d')), "Ukjent."))


            else:
                content = """From: Martin \nTo: Reciever \nSubject: Rusta Vrak Bilutleige. \n\nHei %s,
    Her kommer en kvittering.
    Bookingnummer: %s.
    Fra Dato: %s
    Til Dato: %s
    Pris: %s
    Epost: rusta.vrak@gmail.com
    Telefon +47 400 49 489
                """ % (new_form.first_name, str(booking_id), str(current_booking.initial_date.strftime('%d.%m.%Y')), str(current_booking.final_date.strftime('%d.%m.%Y')), "Ukjent.")

                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()

                mail.starttls()

                mail.login('Nitrax92@gmail.com', 'this.setPw(G)')

                mail.sendmail('Nitrax92@gmail.com', new_form.email, content)

                mail.close()




        return redirect(index)

    else:
        car = get_object_or_404(Car, id=car_id)
        booking = get_object_or_404(Car_Booking, id=booking_id)
        booking_form = BookingRegistrationForm()

        context = {
            'car': car,
            'booking': booking,
            'booking_form': booking_form,
        }

        return render(request, 'cars/booking_form.html', context)

