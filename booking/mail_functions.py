# -*- coding: utf-8 -*-


import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
          <h1> Å Rusta Vrak Bilutleige </h1>
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