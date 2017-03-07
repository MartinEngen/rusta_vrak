# -*- coding: utf-8 -*-
from django.core.mail import send_mail, EmailMessage



def send_mail_django(new_form, current_booking, current_car, price):


    content = """<html>
      <body>
      <h1> Rusta Vrak Bilutleige</h1>
        <p><h3>Hei, %s.</h3><br>
        Dette er en automatisk generert e-post. Vennligst ikke svar på denne e-posten. Henvend deg ved behov til konktaktinformasjonen under i denne eposten. <br> <br>
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
        new_form.customer.first_name.encode('utf8'), str(new_form.id), str(current_car.brand.encode('utf8')),
        str(current_car.model.encode('utf8')), str(current_booking.initial_date.strftime('%d.%m.%Y')),
        str(current_booking.final_date.strftime('%d.%m.%Y')), str(new_form.customer.phone_number), str(price))

    status = send_mail(
        'Rusta Vrak Bilutleige', # Subject
        '',
        '',
        [new_form.customer.email],
        fail_silently=False,
        html_message=content)


    print("EMAIL STATUS: " + str(status))
