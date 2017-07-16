# -*- coding: utf-8 -*-
import logging

from .models import lock_init_final_dates
import datetime


def check_locked_reservation_service_period(initial_date, final_date):
    message = ''
    error = False
    # Any existing locks to stop any reservation getting between two periods of time.
    existing_date_locks = lock_init_final_dates.objects.filter(from_date__gte=datetime.date.today())
    print("Checking for locked service period")

    for locked_period in existing_date_locks:
        print("Checking")
        if locked_period.from_date <= initial_date <= locked_period.to_date:
            message = 'Beklager, vi har ikke mulighet til å levere reservasjonen i denne periode. For mer informasjon ta kontakt'
            error = True

        if locked_period.from_date <= final_date <= locked_period.to_date:
            message = 'Beklager, vi har ikke mulighet til å motta reservasjonen i denne periode. For mer informasjon ta kontakt'
            error = True

    context = {
        'message': message,
        'error': error
    }
    return context