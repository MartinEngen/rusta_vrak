# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, redirect



from .forms import BookingRegistrationForm
from .models import Car, Dates_Reserved, Reservation, Customer

from send_django_mail import send_mail_django
from frontpage.views import index
from data_functions import price_calculator
from reportlab.pdfgen import canvas


import logging


def booking_schema(request, car_id):

    if 'current_booking_id' in request.session:
        current_booking_id = request.session['current_booking_id']
    else:
        # Session has no booking ID, return to the frontpage
        return redirect(index)

    if request.method == 'POST':
        booking_scheme_form = BookingRegistrationForm(request.POST)

        if booking_scheme_form.is_valid():

            # Clean the information from the POST request
            first_name = booking_scheme_form.cleaned_data['first_name']
            last_name = booking_scheme_form.cleaned_data['last_name']
            email = booking_scheme_form.cleaned_data['email']
            phone_number = booking_scheme_form.cleaned_data['phone_number']
            misc_info = booking_scheme_form.cleaned_data['misc_info']

            current_car = get_object_or_404(Car, id=car_id)
            current_booking = get_object_or_404(Dates_Reserved, id=current_booking_id)

            customer, created = Customer.objects.update_or_create(pk=email,
                                                               defaults={'first_name': first_name,
                                                                         'last_name': last_name,
                                                                         'phone_number': phone_number})

            # Increment orders by this user
            customer.num_orders += 1
            customer.save()


            new_reservation, created = Reservation.objects.update_or_create(car_id=car_id,
                                                                   customer=customer,
                                                                   initial_date=current_booking.initial_date,
                                                                   defaults={
                                                                       'misc_info': misc_info,
                                                                       'status': 1, #Status 2 is defined as approved
                                                                       #'initial_date': current_booking.initial_date,
                                                                       'final_date': current_booking.final_date,
                                                                   })

            if created:
                logging.info("New Entry saved, ID: %s, by user %s" % (str(new_reservation.id), customer.email))
            else:
                logging.warning("User has updated an entry. Info: Booking Nr. %s, Customers email: %s" % (str(new_reservation.id), customer.email))


            # TODO: Something has to be done with this table. Maybe figure out some alternative sollution.
            # Deletes the booking dates from the database.
            #current_booking.delete()

            # Calculate
            number_of_days = (new_reservation.final_date - new_reservation.initial_date).days
            price = price_calculator(number_of_days, current_car.price)
            km_included = number_of_days * 50

            # Run the function that handles the sending of receipt.
            send_mail_django(new_reservation, current_booking, current_car, price)
            print(str(customer))
            context = {
                'car': current_car,
                'booking': current_booking,
                'customer': customer,
                'filled_form': new_reservation,
                'price': price,
                'km_included': km_included,
            }

            #Redirect the user to the final page, reciept is shown etc.
            return render(request, 'booking/booking_receipt.html', context)



        # User posted a form which was not valid.
        else:
            error_message = "Feil med gitt informasjon, prøv igjen. "

            form = booking_scheme_form
            car = get_object_or_404(Car, id=car_id)
            booking = get_object_or_404(Dates_Reserved, id=current_booking_id)

            number_of_days = (booking.final_date - booking.initial_date).days
            price = price_calculator(number_of_days, car.price)
            km_included = number_of_days * 50

            context = {
                'car': car,
                'booking': booking,
                'days': number_of_days,
                'price': price,
                'form': form,
                'error_message': error_message,
                'km_included': km_included
            }

            return render(request, 'booking/booking_form.html', context)

    # GET request.
    else:
        car = get_object_or_404(Car, id=car_id)
        booking = get_object_or_404(Dates_Reserved, id=current_booking_id)

        number_of_days = (booking.final_date - booking.initial_date).days
        price = price_calculator(number_of_days, car.price)
        km_included = number_of_days*50


        context = {
            'car': car,
            'booking': booking,
            'days': number_of_days,
            'price': price,
            'km_included': km_included
        }

        return render(request, 'booking/booking_form.html', context)



def download_pdf(request, reservation_id, car_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Rusta_vrak_reservasjon.pdf"'

    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.car_id is not int(car_id):
        return redirect('/')

    reservation_nr = str(reservation.id)
    initial_date = reservation.initial_date.strftime('%d.%m.%Y')
    final_date = reservation.final_date.strftime('%d.%m.%Y')
    bil = str(reservation.car.brand.encode('utf8') + ' ' + reservation.car.model.encode('utf8'))
    car_fuel = str(reservation.car.fuel_type.encode('utf8'))
    car_seats = str(reservation.car.seats)
    car_transmission = str(reservation.car.transmission.encode('utf8'))
    days = (reservation.final_date - reservation.initial_date).days
    calculated_price = price_calculator(days, reservation.car.price)
    pris = str(calculated_price)
    fornavn  = reservation.customer.first_name
    etternavn = reservation.customer.last_name
    kunde = str(fornavn + ' ' + etternavn)

    epost = str(reservation.customer.email)
    tlf = str(reservation.customer.phone_number)


    p = canvas.Canvas(response)
    p.setLineWidth(.5)
    p.setFont('Helvetica', 24)
    p.drawString(60, 780, 'Rusta Vrak Bilutleige')
    p.drawString(60, 750, 'Ordre Bekreftelse')
    #p.setLineWidth(.3)
    #p.setFont('Helvetica', 18)
    #p.drawString(100, 720, 'Bestilling')
    #p.line(20, 710, 580, 710)
    p.setLineWidth(.5)

    p.line(20, 705, 580, 705)
    p.setFont('Helvetica', 16)
    p.drawString(60, 690, 'Reservasjonen')
    p.setFont('Helvetica', 13)
    p.drawString(80, 675, 'Reservasjon Nr')
    p.setLineWidth(.3)
    p.drawString(350, 675, reservation_nr)
    p.drawString(80, 655, 'Hente Dato: ')
    p.drawString(350, 655, initial_date)
    p.drawString(80, 640, 'Leveres Dato:')
    p.drawString(350, 640, final_date)

    p.line(20, 620, 580, 620)

    p.setFont('Helvetica', 16)
    p.drawString(60, 600, 'Bilen')
    p.setFont('Helvetica', 13)
    p.drawString(80, 585, bil)
    #p.setLineWidth(.3)
    p.drawString(350, 570, car_fuel)
    p.drawString(80, 570, 'Drivstoff')

    p.drawString(350, 555, car_seats)
    p.drawString(80, 555, 'Antall Seter')


    p.drawString(80, 540, 'Girkasse')
    p.drawString(350, 540, car_transmission)





    p.line(20, 530, 580, 530)
    p.setFont('Helvetica', 16)
    p.drawString(60, 500, 'Kunde Opplysninger')

    p.setFont('Helvetica', 13)
    p.drawString(80, 480, 'Navn')
    p.drawString(350, 480, kunde)

    p.drawString(80, 465, 'Epost')
    p.drawString(350, 465, epost)

    p.drawString(80, 450, 'Telefon Nummer')
    p.drawString(350, 450, tlf)




    p.line(20, 445, 580, 445)
    p.setFont('Helvetica', 16)



    p.drawString(60, 75, 'Kontakt Informasjon')
    p.setFont('Helvetica', 14)
    p.drawString(80, 60, 'Epost adresse: rusta.vrak@gmail.com')
    p.drawString(80, 45, 'Telefon +47 400 49 489')



    p.showPage()
    p.save()
    return response
