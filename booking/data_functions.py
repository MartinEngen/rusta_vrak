# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse
from reportlab.pdfgen import canvas

import json
import datetime

def generate_calendar_data(finalized_bookings):
    data = []

    for finalized_bookings in finalized_bookings:
        start_date = finalized_bookings.car_date_reservation.initial_date
        end_date = finalized_bookings.car_date_reservation.final_date

        event = {'start': str(start_date), 'end': str(end_date + datetime.timedelta(days=1)), 'rendering': 'background',
                 'color': 'black'}


        data.append(event)

    """
    for booking in car_bookings:
        start_date = booking.initial_date
        end_date = booking.final_date

        event = {'start': str(start_date), 'end': str(end_date + datetime.timedelta(days=1)), 'rendering': 'background',
                 'color': 'black'}
        data.append(event)
    """


    json_data_string = json.dumps(data)
    return json_data_string


def generate_pdf():
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




def price_calculator(days, car):
    start_price = car.price

    price = 250

    """
    if days < 4:
        price = 250 * days

    elif days > 4 and days < 10:
        price = (250 * days)* 0.9

    elif days > 9 and days < 15:
        price = (250 * days) * 0.7

    elif days > 14 and days < 20:
        price = (250 * days) * 0.5

    elif days > 19 and days < 25:
        price = (250 * days) * 0.4

    elif days > 24 and days < 30:
        price = (250 * days) * 0.35
    else:
        price = 2500
    """
    # TODO: Add functionality to set correct number after longer rent discount
    return start_price*days