# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, redirect



from .forms import BookingForm, BookingRegistrationForm
from .models import Car, Dates_Reserved, Reservation, Customer


from frontpage.views import index


#custom functions
from data_functions import generate_calendar_data, price_calculator, generate_pdf
from mail_functions import send_mail_receipt

#PDF generator
from reportlab.pdfgen import canvas
import datetime



def booking_schema(request, car_id):


    current_booking_id = request.session['current_booking_id']

    if not current_booking_id:
        # Session has no booking ID, return to frontpage..
        return redirect('/')

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


            new_form = Reservation(car_id=car_id, dates_reserved_id=current_booking_id,
                                   customer=customer, misc_info=misc_info, status=2)

            new_form.save()

            number_of_days = (current_booking.final_date - current_booking.initial_date).days + 1

            # Run the function that handles the sending of receipt.
            send_mail_receipt(new_form, current_booking, current_booking_id, current_car)

            price = price_calculator(number_of_days, current_car.price)
            context = {
                'car': current_car,
                'booking': current_booking,
                'filled_form': new_form,
                'price': price,
            }

            #Redirect the user to the final page, reciet is shown etc.
            return render(request, 'booking/booking_receipt.html', context)



        # User posted a form which was not valid.
        else:
            return redirect(index)

    else:
        car = get_object_or_404(Car, id=car_id)
        booking = get_object_or_404(Dates_Reserved, id=current_booking_id)

        number_of_days = (booking.final_date - booking.initial_date).days + 1
        price = price_calculator(number_of_days, car.price)


        context = {
            'car': car,
            'booking': booking,
            'days': number_of_days,
            'price': price
        }

        return render(request, 'booking/booking_form.html', context)



def download_pdf(request, reservation_id):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Kvittering.pdf"'

    booking = get_object_or_404(Reservation, id=reservation_id)

    booking_nr = str(booking.id)
    initial_date = str(booking.car_date_reservation.initial_date)
    final_date = str(booking.car_date_reservation.final_date)
    bil = str(booking.car.brand.encode('utf8') + ' ' + booking.car.model.encode('utf8'))
    days = (booking.car_date_reservation.final_date - booking.car_date_reservation.initial_date).days
    calculated_price = price_calculator(days, booking.car.price)
    pris = str(calculated_price)
    fornavn  = booking.first_name
    etternavn = booking.last_name
    kunde = str(fornavn + ' ' + etternavn)

    epost = str(booking.email)
    tlf = str(booking.phone_number)


    p = canvas.Canvas(response)
    p.setLineWidth(.5)
    p.setFont('Helvetica', 34)
    p.drawString(100, 750, 'Rusta Vrak Bilutleige')
    p.setLineWidth(.3)
    p.setFont('Helvetica', 24)
    p.drawString(100, 720, 'Kvittering')
    p.line(20, 710, 580, 710)
    p.setLineWidth(.5)
    p.setFont('Helvetica', 16)
    p.drawString(100, 680, 'Booking Nr. ')
    p.setLineWidth(.3)
    p.drawString(350, 680, booking_nr)
    p.drawString(100, 650, 'Hentes: ')
    p.drawString(350, 650, initial_date)

    p.drawString(100, 620, 'Leveres: ')
    p.drawString(350, 620, final_date)

    p.line(20, 600, 580, 600)
    p.drawString(100, 570, 'Bil:..')
    p.drawString(350, 570, bil)

    p.drawString(100, 550, 'Pris')
    p.drawString(350, 550, pris)

    p.line(20, 530, 580, 530)
    p.drawString(100, 510, 'Kunde')
    p.drawString(350, 510, kunde)

    p.drawString(100, 480, 'Epost')
    p.drawString(350, 480, epost)

    p.drawString(100, 450, 'Telefon Nummer')
    p.drawString(350, 450, tlf)


    p.showPage()
    p.save()
    return response


def prisTest(request):

    return render(request, 'booking/pristest.html')