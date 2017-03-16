# -*- coding: utf-8 -*-
from control_panel.models import lock_reservation_period

import json
import datetime


def generate_booked_dates(finalized_bookings):
    """ Generate data for the datepickers. """
    # Gathering all locked dates and converts this into a JSON object.
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

        for i in range(delta.days + 1):
            locked_date = locked_period.from_date + datetime.timedelta(days=i)
            data.append(locked_date.strftime('%d.%m.%Y'))

    json_data_string = json.dumps(data)
    return json_data_string


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
