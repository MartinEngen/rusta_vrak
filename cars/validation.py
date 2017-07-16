# -*- coding: utf-8 -*-
import logging
from django.db.models import Q

from booking.models import Reservation
from control_panel.models import lock_reservation_period

import datetime


# Validate dates before reservation.
def validate_availability(reserved_initial_date, reserved_final_date, registered_reservations):
    message = ''
    error = False

    for finalized_booking in registered_reservations:
        # Checks if the date is placed within a range of already booked.
        if finalized_booking.initial_date <= reserved_initial_date <= finalized_booking.final_date or finalized_booking.initial_date <= reserved_final_date <= finalized_booking.final_date:
            logging.error("Error, not able to book. Overlapping")
            message = "Reservasjon overlapper, velg en ledig periode."
            context = {
                'message': message,
                'error': True
            }
            return context

        # Check if there is an exisiting booking within this new entry.
        if reserved_initial_date <= finalized_booking.initial_date <= reserved_final_date or reserved_initial_date <= finalized_booking.final_date <= reserved_final_date:
            logging.error("Error, not able to book. Overlapping")
            message = "Reservasjon overlapper, velg en ledig periode."
            context = {
                'message': message,
                'error': True
            }
            return context

    # All locked periods.
    existing_reservation_locks = lock_reservation_period.objects.filter(to_date__gte=datetime.date.today())
    for locked_periods in existing_reservation_locks:

        if locked_periods.from_date <= reserved_initial_date <= locked_periods.to_date or locked_periods.from_date <= reserved_final_date <= locked_periods.to_date:
            logging.error("Error, not able to book. Locked Period")
            message = "Reservasjon overlapper, velg en ledig periode."
            context = {
                'message': message,
                'error': True
            }
            return context

        if reserved_initial_date <= locked_periods.from_date <= reserved_final_date or reserved_initial_date <= locked_periods.to_date <= reserved_final_date:
            logging.error("Error, not able to book. Locked Period")
            message = "Reservasjon overlapper, velg en ledig periode."
            context = {
                'message': message,
                'error': True
            }
            return context

    context = {
        'message': message,
        'error': error
    }
    return context


# Used for both validating search dates, as well as new reservations into the system.
def validate_date(initial_date, final_date):
    message = ''
    error = False
    # Less than 1 day booked, abort.
    if (final_date - initial_date).days < 1:
        logging.error("Less than 1 day, stop")
        message = "For liten leieperiode."
        error = True

    # Final date before the initial date.
    # A possible solution would be to simply swap the dates.
    if final_date < initial_date:
        logging.info("Final date is before initial date")
        message = "Leveringsdagen er satt før Hente dagen, Prøv på nytt."
        error = True

    if (initial_date < datetime.date.today()+ datetime.timedelta(days=2)):
        message = "Kan ikke registrere en reservasjon såpass nærme hentedato. Ta kontakt på epost eller telefon for å gjennomføre denne reservasjonen"
        error = True

    # More than 30 days booked, tell user to contact instead.
    if (final_date - initial_date).days > 30:
        logging.error("Logging more than 30 days, Stop.")
        message = "Kan ikke reservere større enn 30 dagers reservasjoner. Ta kontakt for en større reservasjon."
        error = True

    # User tries to book from before today, this is illegal.
    if initial_date < datetime.date.today():
        message = "Kan ikke registerer en reservasjon tilbake i tid."
        error = True

    context = {
        'message': message,
        'error': error
    }
    return context


# Find all available cars between two dates, from a list of cars.
def find_available_cars(initial_date, final_date, cars):

    # Check if there is some locked period within the searched dates.
    # No available cars in this period, so return before checking the individual cars.

    # All relevant locked periods.
    existing_reservation_locks = lock_reservation_period.objects.filter(to_date__gte=datetime.date.today())
    if existing_reservation_locks:
        # Check for overlapping in any locked periods.
        # See details for how this works below, it is identical to checking the periods of any existing reservations.
        init_overlapping_locks = existing_reservation_locks.filter(Q(from_date__lte=initial_date) & Q(to_date__gte=initial_date))
        fin_overlapping_locks = existing_reservation_locks.filter(Q(from_date__lte=final_date) & Q(to_date__gte=final_date))
        inside_overlapping_locks = existing_reservation_locks.filter(Q(from_date__gte=initial_date) & Q(to_date__lte=final_date))

        # If any overlaps detected, return an empty list.
        if init_overlapping_locks or fin_overlapping_locks or inside_overlapping_locks:

            return []

    # All reservations of the cars
    car_reservations = Reservation.objects.filter(car__in=cars)

    # Checking if the given dates is between or same as any dates already reserved.

    # If any overlapping by the reserved 'initial_date'(s)
    # Catches all overlapped as displayed:
    # (Ri = Reserved Initial Date, In = searched 'initial_date', Fi = searched 'final_date', _=Date)
    # [_,_,In,_,Ri,Fi,_,_,_,..]
    # [_,In,_,_,Ri/Fi,_,_,_,..]
    # [_,_,_,_,Ri/In,_,Fi,_,..]
    init_booking_overlap = car_reservations.filter(Q(initial_date__lte=initial_date) & Q(final_date__gte=initial_date))

    # If any overlapping by the reserved 'final_date'(s)
    # Catches all overlapped as displayed:
    # (Rf = Reserved Final Date, In = searched 'initial_date', Fi = searched 'final_date', _=Date)
    # [_,_,In,_,Rf,Fi,_,_,_,..]
    # [_,In,_,_,Rf/Fi,_,_,_,..]
    # [_,_,_,_,Rf/In,_,Fi,_,..]
    fin_booking_overlap = car_reservations.filter(Q(initial_date__lte=final_date) & Q(final_date__gte=final_date))

    # If any overlapping by the reserved periods. Checks for any overlapping between Initial Date and Final Date
    # Catches all overlapped as displayed:
    # (Ri & Rf = Reserved Dates, In = searched 'initial_date', Fi = searched 'final_date', _=Date)
    # [_,_,Ri,In,_,_,_,_,_,_,Fi,Rf,_,_,..]
    # [_,_,Ri/In,_,_,_,_,_,_,Rf/Fi,_,_,..]
    # [_,_,Ri,_,_,_,In,_,Fi,_,_,Rf,_,_,..]
    inside_booking_overlap = car_reservations.filter(Q(initial_date__gte=initial_date) & Q(final_date__lte=final_date))

    # Removes all detected overlaps.
    available_cars = cars\
        .exclude(id__in=init_booking_overlap.values("car_id"))\
        .exclude(id__in=fin_booking_overlap.values("car_id"))\
        .exclude(id__in=inside_booking_overlap.values("car_id"))

    return available_cars

