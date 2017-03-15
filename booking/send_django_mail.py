# -*- coding: utf-8 -*-
from django.core.mail import send_mail, EmailMessage
import datetime


def send_mail_django(new_form, current_booking, current_car, price):


    content = """<html>
<head>
    <meta charset="utf-8">
    <title>Rusta Vrak Bilutleige</title>
	<style>
table {
    border-collapse: collapse;
    width: 50%%;
}

td{
    border: 1px solid #bcbaba;
    text-align: left;
    padding: 8px;
}
th{
    font-size: larger;
}

tr:nth-child(even) {
    background-color: #dddddd;
}

body{
	padding: 10px;
	font-family: arial, sans-serif;
}

</style>
</head>
    <body>
      <h1> Rusta Vrak Bilutleige</h1>
	  <p>Dette er ein automatisk generert e-post. Ikkje svar på denne e-posten.</p>
        <h3>Hei, %s.</h3>
        <p>Din reservasjon er motteken. <br>
		Reservasjonen ligg no I vårt system og du vil bli kontakta for ein endeleg bekreftelse.</p>
		<br>
		<table>
			<tr>
				<th>Informasjon om reservasjonen</th>
			</tr>
			<tr style="background-color: #dddddd;">
				<td><b>Reservasjonsnummer</b></td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Bil</td>
				<td>%s %s</td>
			</tr>
			<tr style="background-color: #dddddd;">
				<td>Hentast dato</td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Tilbakeleverast dato</td>
				<td>%s</td>
			</tr>
			<tr style="background-color: #dddddd;">
				<td>Registert telefonnummer</td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Pris</td>
				<td>%s kr</td>
			</tr>

		</table>

        <hr>
        <p>Leigetakar av bilen har plikt om å bevise at ein har gyldig førarkort, derfor ber vi deg sende eit bilete av ditt førarkort til vår e-postadresse: Rusta.vrak@gmail.com</p>
		<div id="contact">
			<p style="font-size: 53px">
				<h2>Kontakt: </h2>
				<p>E-post: Rusta.vrak@gmail.com <br>
				Telefon: +47 400 49 489</p>
			</p>
		</div>

</body>
</html>""" % (
        new_form.customer.first_name.encode('utf8'),  #Greeting
        str(new_form.id),  # Reservation Info Table
        str(current_car.brand.encode('utf8')),
        str(current_car.model.encode('utf8')),
        str(current_booking.initial_date.strftime('%d.%m.%Y')),
        str(current_booking.final_date.strftime('%d.%m.%Y')),
        str(new_form.customer.phone_number),
        str(price)
    )

    status = send_mail(
        'Rusta Vrak Bilutleige', # Subject
        '',
        '',
        [new_form.customer.email],
        fail_silently=False,
        html_message=content)





    # Send email to alert rustavrak about the new reservation
    days_until_deliver = (current_booking.initial_date - datetime.date.today()).days
    alert_content = """<html>
<head>
    <meta charset="utf-8">
	<title>NY Bestilling.</title>

	<style>
table {
    border-collapse: collapse;
    width: 50%%;
}

td{
    border: 1px solid #bcbaba;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}

#contact{

}

body{
	padding: 10px;
	font-family: arial, sans-serif;
}

</style>
</head>

<body>
      <h1> Rusta Vrak Bilutleige - Reservasjon Registerert</h1>
	  <p>Dette er ein automatisk generert e-post. Ikkje svar på denne e-posten.</p>
        <h3>Det har kommet en ny reservasjon på rustavrak.no</h3>
		<p> Denne nye reservasjonen ønsker å hente %s %s på dato %s, (Om %s Dager)</p>
		<table style="border-collapse: collapse;width: 50%%;">
			<tr>
				<th>Informasjon om reservasjonen</th>
			</tr>
			<tr>
				<td>Reservasjonsnummer</td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Bil</td>
				<td>%s %s</td>
			</tr>

			<tr>
				<td>Hentast dato</td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Tilbakeleverast dato</td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Pris</td>
				<td>%s kr</td>
			</tr>

			<tr>
				<td>Kunde</td>
				<td>%s %s</td>
			</tr>
            <tr>
				<td>Registert telefonnummer</td>
				<td>%s</td>
			</tr>
			<tr>
				<td>Epost</td>
				<td>%s</td>
			</tr>

		</table>

        <hr>
		<h3>For å endre status på ordre</h3>
		 <ol>
		  <li>Logg inn på Admin. <a href="http://www.rustavrak.no/admin/">Rustavrak admin</a></li>
		  <li>Gå på Reservasjoner (Under 'BOOKING')</li>
		  <li>Klikk på ID til gjeldene reservasjon. (Dette tilsvarer Reservasjonsnummer)</li>
		  <li>Dobbelsjekk at dato, kunde og bil stemmer.</li>
		  <li>Endre feltet Ordrestatus. En Ny ordre vil automatisk ha status Pending, her kan man velge enten Approved eller Declined. </li>
		  <li>Save. </li>
		  <li>Gi beskjed til Kunde.</li>
		</ol>

		<h5>Bare ring vist det er noen problemer</h5>
</body>
</html>""" % (
            str(current_car.brand.encode('utf8')),
            str(current_car.model.encode('utf8')),
            str(current_booking.initial_date.strftime('%d.%m.%Y')),
            str(days_until_deliver),

            str(new_form.id),  # RESERVATION DETAILS
            str(current_car.brand.encode('utf8')),
            str(current_car.model.encode('utf8')),
            str(current_booking.initial_date.strftime('%d.%m.%Y')),
            str(current_booking.final_date.strftime('%d.%m.%Y')),
            str(price),

            new_form.customer.first_name.encode('utf8'),  # CUSTOMER
            new_form.customer.last_name.encode('utf8'),
            str(new_form.customer.phone_number),
            str(new_form.customer.email),
            )

    alert_mail = send_mail(
        'Reservasjon Registrert. Rustavrak. (Ønskes hentes om %s dager)' % str(days_until_deliver),  # Subject
        '',
        '',
        ['rusta.vrak@gmail.com'],
        fail_silently=False,
        html_message=alert_content
    )
