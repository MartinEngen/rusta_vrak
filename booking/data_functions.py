
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



def price_calculator(days):
    start_price = 250

    price = 250

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

    # TODO: Add functionality to set correct number after longer rent discount
    return price