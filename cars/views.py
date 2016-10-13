# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse


from django.shortcuts import get_object_or_404, redirect


from .forms import BookingForm, BookingRegistrationForm

from .models import Car, Car_Booking, Registration_Scheme
import logging
import datetime
import json
from django.core import serializers
from django.http import JsonResponse

from frontpage.views import index

# Mail API's
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Uniqueness
import hashlib

# TODO: Genereal Code Cleanup. This may entail moving some functions to new apps / files.
def personal_car(request):

    print(hash)
    personal_cars = Car.objects.filter(car_type=1)
    context = {
        'personal_cars': personal_cars,
    }
    return render(request, 'cars/personal_cars.html', context)


def car_availability(request, car_id):

    if request.method == 'POST':

        booking_form = BookingForm(request.POST)

        # logging.info("Booking Requested.")
        print ("Booking Requested.")
        car = get_object_or_404(Car, id=car_id)
        if booking_form.is_valid():
            print("Valid")

            initial_date = booking_form.cleaned_data['initial_date']
            final_date = booking_form.cleaned_data['final_date']

            # Check if the number of days exeeds 30 days.
            # Get all registered bookings for this car.
            car_bookings = Car_Booking.objects.filter(car=car).exclude(final_date__lte=datetime.date.today()).order_by(
                'initial_date')

            if (final_date - initial_date).days > 30:
                logging.error("Logging more than 30 days, Stop.")
                message = "Kan ikke reservere mer enn 30 dager i gangen. Ta kontakt for en større reservasjon."

                calendar_data = generate_calendar_data(car_bookings)

                context = {
                    'car': car,
                    'bookings': car_bookings,
                    'warning': True,
                    'message': message,
                    'json_data_string': calendar_data,
                }



                return render(request, 'cars/spesific_car.html', context)




            # User tries to book from before today, this is illegal.
            if initial_date < datetime.date.today():
                logging.error("Error, not able to book.")
                message = "Kan ikke registerer en reservasjon som går tilbake i tid."

                calendar_data = generate_calendar_data(car_bookings)

                context = {
                    'car': car,
                    'bookings': car_bookings,
                    'warning': True,
                    'message': message,
                    'json_data_string': calendar_data,
                }


                return render(request, 'cars/spesific_car.html', context)

            # Check if the dates are valid, this means that all the dates inbetween are also not already booked.
            for booking in car_bookings:
                if booking.initial_date <= initial_date and booking.final_date >= initial_date or booking.initial_date <= final_date and booking.final_date >= final_date:
                    logging.error("Error, not able to book.")
                    message = "Reservasjon overlapper, velg en ledig periode."

                    calendar_data = generate_calendar_data(car_bookings)

                    context = {
                        'car': car,
                        'bookings': car_bookings,
                        'warning': True,
                        'message': message,
                        'json_data_string': calendar_data,
                    }

                    return render(request, 'cars/spesific_car.html', context)

            new_booking = Car_Booking(car=car, initial_date=booking_form.cleaned_data['initial_date'], final_date=booking_form.cleaned_data['final_date'], status=2)
            new_booking.save()


            return redirect('cars:booking_scheme', booking_id=new_booking.id, car_id=car.id)


        else:

            print("Not Valid.")
            logging.debug("Non valid form posted.")
            print(booking_form.errors)

            car_bookings = Car_Booking.objects.filter(car=car)
            return render(request, 'cars/spesific_car.html', {'car': car, 'bookings': car_bookings, 'errors': booking_form.errors})

    else:

        current_car = get_object_or_404(Car, id=car_id)

        images_string = current_car.gallery_images
        images = images_string.split(',')

        # Gather the information required by the Calendar
        car_bookings = Car_Booking.objects.filter(car=current_car).exclude(final_date__lte=datetime.date.today()).order_by('initial_date')

        calendar_data = generate_calendar_data(car_bookings)

        context = {
            'car': current_car,
            'bookings': car_bookings,
            'json_data_string': calendar_data,
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



            number_of_days = (current_booking.final_date - current_booking.initial_date).days + 1
            print("Dager: " + str(number_of_days))

            print(number_of_days * 250)


            # Run the function that handles the sending of receipt.
            send_mail_receipt(new_form, current_booking, booking_id, current_car)

            price = price_calculator(number_of_days)
            context = {
                'car': current_car,
                'booking': current_booking,
                'filled_form': new_form,
                'price': price,
            }

            #Redirect the user to the final page, reciet is shown etc.
            return render(request, 'cars/booking_receipt.html', context)
            #return redirect(booking_receipt(request, current_booking, new_form))







        return redirect(index)

    else:
        car = get_object_or_404(Car, id=car_id)
        booking = get_object_or_404(Car_Booking, id=booking_id)
        #booking_form = BookingRegistrationForm()

        number_of_days = (booking.final_date - booking.initial_date).days
        price = price_calculator(number_of_days)


        context = {
            'car': car,
            'booking': booking,
            'days': number_of_days,
            'price': price
            #'booking_form': booking_form,
        }

        return render(request, 'cars/booking_form.html', context)


def generate_calendar_data(car_bookings):
    data = []

    for booking in car_bookings:
        start_date = booking.initial_date
        end_date = booking.final_date

        event = {'start': str(start_date), 'end': str(end_date + datetime.timedelta(days=1)), 'rendering': 'background',
                 'color': 'black'}
        data.append(event)

    json_data_string = json.dumps(data)
    return json_data_string



def abort_booking_with_error(request,car, car_bookings, message):
    calendar_data = generate_calendar_data(car_bookings)

    context = {
        'car': car,
        'bookings': car_bookings,
        'warning': True,
        'message': message,
        'json_data_string': calendar_data,
    }
    print("Abort, Abort.")
    return redirect(index)
    return render(request, 'cars/spesific_car.html', context)





def booking_receipt(request, booking_id, registration_id):
    # TODO: Get the information required for the receipt page. Send this to the view and display it.



    return render(request, 'cars/booking_receipt.html')



def price_calculator(days):
    start_price = 250

    # TODO: Add functionality to set correct number after longer rent discoun

    return start_price * days




def send_mail_receipt(new_form, current_booking, booking_id, current_car):

    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
        from google.appengine.api import mail

        content = """\
        <html>
          <head>Rusta Vrak Bilutleige</head>
          <body>
          <h1> Rusta Vrak Bilutleige </h1>
            <p><h3>Hei, %s.</h3><br>
            Her kommer en kvittering fra din reservasjon av leiebil. <br>
                <hr>
                <b>Bookingsnummer: %s </b><br>
                %s %s <br>
                Hentes dato: %s <br>
                Leveres dato: %s <br>
                Registert Telefonnummer: %s <br>
                Pris: (Under Arbeid.) <br>
            </p>
            <hr>
            <p style="font-size: 53px">
                <h4>Kontakt: </h4>
                Epost: Rusta.vrak@gmail.com <br>
                Telefon: +47 400 49 489
            </p>
          </body>
        </html>
        """ % (
        new_form.first_name.encode('utf8'), str(booking_id),str(current_car.brand.encode('utf8')), str(current_car.model.encode('utf8')), str(current_booking.initial_date.strftime('%d.%m.%Y')),
        str(current_booking.final_date.strftime('%d.%m.%Y')), str(new_form.phone_number))

        msg = MIMEText(content, 'html')




        logging.debug("Sending From Google Mail API")
        mail.send_mail(sender='Nitrax92@gmail.com',
                       to="%s %s <%s>" % (new_form.first_name, new_form.last_name, new_form.email),
                       subject="Kvittering. Rusta Vrak Bilutleige",
                       body="",
                       html=msg.as_string())

        logging.debug("Sending, complete.")

    else:

        content = """\
                <html>
          <head></head>
          <body>
          <h1> Å RRusta Vrak Bilutleige </h1>
            <p><h3>Hei, %s.</h3><br>
            Her kommer en kvittering fra din reservasjon av leiebil. <br>
                <hr>
                <b>Bookingsnummer: %s </b><br>
                Fra Dato: %s <br>
                Til Dato: %s <br>
                Registert Telefonnummer: %s <br>
                Pris: (Under Arbeid.) <br>
            </p>
            <hr>
            <p style="font-size: 53px">
                <h4>Kontakt: </h4>
                Epost: Rusta.vrak@gmail.com <br>
                Telefon: +47 400 49 489
            </p>
          </body>
        </html>
        """ % (new_form.first_name.encode('utf8'), str(booking_id), str(current_booking.initial_date.strftime('%d.%m.%Y')),
               str(current_booking.final_date.strftime('%d.%m.%Y')), str(new_form.phone_number))
        msg = MIMEText(content, 'html')

        msg['Subject'] = 'Rusta Vrak Bilutleige. Kvittering.'
        msg['From'] = 'Nitrax92@gmail.com'
        msg['To'] = new_form.email
        msg['Content-Type'] = "text/html; charset=UTF-8"
        msg['Content-Transfer-Encoding'] = "quoted-printable"

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()

        mail.starttls()

        mail.login('Nitrax92@gmail.com', 'this.setPw(G)')

        mail.sendmail('Nitrax92@gmail.com', new_form.email, msg.as_string())

        mail.close()