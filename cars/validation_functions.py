# -*- coding: utf-8 -*-
import logging
from django.db.models import Q

from booking.models import Reservation

import datetime




# Validate dates before reservation.
# Used for both validating search dates, as well as new reservations into the system.
def validate_date(initial_date, final_date):

    message = ''
    error = False


      # Less than 1 day booked, abort.
    if (final_date - initial_date).days < 1:
        logging.error("Less than 1 day, stop")
        message = "For liten leieperiode."
        error = True


    # Final date before the inital date.
    if (final_date < initial_date):
        logging.info("Final date is before initial date")
        message = "Leveringsdagen er satt før Hente dagen, Prøv på nytt."
        error = True
        # calendar_data = generate_calendar_data(finalized_bookings)


        # More than 30 days booked, tell user to Contact instead.
    if (final_date - initial_date).days > 30:
        logging.error("Logging more than 30 days, Stop.")
        message = "Kan ikke reservere mer enn 30 dager i gangen. Ta kontakt for en større reservasjon."
        error = True


        # User tries to book from before today, this is illegal.
    if initial_date < datetime.date.today():
        logging.error("Error, not able to book.")
        message = "Kan ikke registerer en reservasjon tilbake i tid."
        error = True


    context = {
        'message': message,
        'error': error
    }

    return context

# Find all avaiable cars between two dates, from a list of cars.
def find_available_cars(inital_date, final_date, cars):
    # All reservations of the cars
    car_reservations = Reservation.objects.filter(car__in=cars)

    # Checking if the dates input is between or same as any dates already reserved.
    init_booking_overlap = car_reservations.filter(Q(initial_date__lte=inital_date) & Q(final_date__gte=inital_date))
    fin_booking_overlap = car_reservations.filter(Q(initial_date__lte=final_date) & Q(final_date__gte=final_date))

    available_cars = cars.exclude(id__in=init_booking_overlap.values("car_id")).exclude(id__in=fin_booking_overlap.values("car_id"))

    return available_cars