# -*- coding: utf-8 -*-


import logging

from booking.models import Reservation
import datetime




# Validate dates before reservation.
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
        message = "Leveringsdagen er satt før Hente dagen, gjør om og prøv på nytt."
        error = True
        # calendar_data = generate_calendar_data(finalized_bookings)


        # More than 30 days booked, abort.
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

    #Overlapping by final date
    final_date_booking_overlap = car_reservations.filter(dates_reserved__final_date__range=(inital_date, final_date))

    # Overlapping by inital date
    initial_date_booking_overlap = car_reservations.filter(dates_reserved__initial_date__range=(inital_date, final_date))

    print("Overlapping: " + str(final_date_booking_overlap.count()) + " " + str(initial_date_booking_overlap.count()))

    # Remove the cars with overlapping dates
    available_cars = cars.exclude(reserved_car__booking__car_id__in=final_date_booking_overlap.values("car_id")).exclude(
        reserved_car__booking__car_id__in=initial_date_booking_overlap.values("car_id"))

    return available_cars