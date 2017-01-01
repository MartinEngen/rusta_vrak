# -*- coding: utf-8 -*-


import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging


def send_mail_receipt(new_form, current_booking, booking_id, current_car, price):

    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
        from google.appengine.api import mail

        content = """<html>
              <head>Rusta Vrak Bilutleige</head>
          <body>
          <h1> Rusta Vrak Bilutleige </h1>
            <p><h3>Hei, %s.</h3><br>
            Her kommer en bekreftelse fra din reservasjon av leiebil. <br>
                <hr>
                <b>Bookingsnummer: %s </b><br>
                %s %s <br>
                Hentes dato: %s <br>
                Leveres dato: %s <br>
                Registert Telefonnummer: %s <br>
                Pris: %s <br>
            </p>
            <hr>
            <p>Leier av bilen har plikt om å bevise at man har gyldig førerkort, derfor ber vi deg sende et bilde av ditt førerkort til vår epostadresse: Rusta.vrak@gmail.com</p>
            <p style="font-size: 53px">
                <h4>Kontakt: </h4>
                Epost: Rusta.vrak@gmail.com <br>
                Telefon: +47 400 49 489
            </p>
          </body>
        </html>
        """ % (
        new_form.customer.first_name.encode('utf8'), str(booking_id),str(current_car.brand.encode('utf8')), str(current_car.model.encode('utf8')), str(current_booking.initial_date.strftime('%d.%m.%Y')),
        str(current_booking.final_date.strftime('%d.%m.%Y')), str(new_form.customer.phone_number), str(price))

        msg = MIMEText(content, 'html')




        logging.debug("Sending From Google Mail API")
        mail.send_mail(sender='Nitrax92@gmail.com',
                       to="%s %s <%s>" % (new_form.customer.first_name, new_form.customer.last_name, new_form.customer.email),
                       subject="Bekreftelse. Rusta Vrak Bilutleige",
                       body="Body",
                       html=content)

        logging.debug("Sending, complete.")

    else:
        pass