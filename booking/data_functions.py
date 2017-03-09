# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse
from reportlab.pdfgen import canvas

from control_panel.models import lock_reservation_period

import json
import datetime


def generate_booked_dates(finalized_bookings):
    data = []
    for booking in finalized_bookings:
        delta = booking.final_date - booking.initial_date

        for i in range(delta.days + 1):
            booked_date = booking.initial_date + datetime.timedelta(days=i)
            data.append(booked_date.strftime('%d.%m.%Y'))

    # Add any locked periods
    existing_reservation_locks = lock_reservation_period.objects.filter(to_date__gte=datetime.date.today())
    for locked_period in existing_reservation_locks:
        delta = locked_period.to_date - locked_period.from_date
        print("locked period existing.")

        for i in range(delta.days + 1):
            locked_date = locked_period.from_date + datetime.timedelta(days=i)
            data.append(locked_date.strftime('%d.%m.%Y'))

    json_data_string = json.dumps(data)
    return json_data_string


def generate_pdf(customer, filled_form):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Kvittering.pdf"'

    booking_nr = str(10)
    initial_date = str(datetime.date.today())
    final_date = str(datetime.date.today())
    bil = str('Citroën' + ' ' + 'Xanita')
    pris = str(500)
    fornavn = 'Martin'
    etternavn = 'Engen'
    kunde = str(fornavn + ' ' + etternavn)

    epost = str('Nitrax92@gmail.com')
    tlf = str(46966993)

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

    # print(p.getAvailableFonts())

    # p.drawString(30, 703, 'RECEIVED BY:')
    # p.line(120, 700, 580, 700)
    # p.drawString(120, 703, b)






    p.showPage()
    p.save()
    return response


def price_calculator(days, start_price):
    # Round to closest 5
    def round_function(x, base=5):
        return int(base * round(float(x) / base))

    if 0 <= days <= 29:
        # Initialize variables
        discount_calculated = 1         # Initialize to 0% discount.
        amount_of_discounts = days / 5  # Number of discount chunks.
        discount = 0.825                # 17.5% discount for each chunk

        # Iterate through the chunks, adding a 17.5% discount to the existing discount.
        for i in range(0, amount_of_discounts):
            discount_calculated *= discount

        final_price = round_function(start_price*days*discount_calculated)

    else:
        # 30 days rented, final price is 2500 for the normal priced cars.
        if start_price == 250:
            final_price = 2500

        #
        else:
            final_price = 2750

    return final_price
