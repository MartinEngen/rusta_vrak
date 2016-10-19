# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse


from django.shortcuts import get_object_or_404, redirect


from .forms import BookingForm, BookingRegistrationForm

from .models import Car, Car_Date_Reservation, Registration_Schema


from frontpage.views import index


#custom functions
from data_functions import generate_calendar_data, price_calculator
from mail_functions import send_mail_receipt



def booking_schema(request, booking_id, car_id):

    if request.method == 'POST':

        booking_scheme_form = BookingRegistrationForm(request.POST)

        if booking_scheme_form.is_valid():
            print("Valid")
            first_name = booking_scheme_form.cleaned_data['first_name']
            last_name = booking_scheme_form.cleaned_data['last_name']

            email = booking_scheme_form.cleaned_data['email']
            phone_number = booking_scheme_form.cleaned_data['phone_number']
            misc_info = booking_scheme_form.cleaned_data['misc_info']

            current_car = get_object_or_404(Car, id=car_id)
            current_booking = get_object_or_404(Car_Date_Reservation, id=booking_id)

            new_form = Registration_Schema(car_id=car_id, car_date_reservation_id=booking_id,
                                           email=email, phone_number=phone_number, first_name=first_name,
                                           last_name=last_name, misc_info=misc_info)
            new_form.save()



            number_of_days = (current_booking.final_date - current_booking.initial_date).days + 1
            print("Dager: " + str(number_of_days))

            print(number_of_days * 250)


            # Run the function that handles the sending of receipt.
            send_mail_receipt(new_form, current_booking, booking_id, current_car)

            price = price_calculator(number_of_days)
            context = {
                'car': current_car,
                'booking': current_booking,
                'filled_form': new_form,
                'price': price,
            }

            #Redirect the user to the final page, reciet is shown etc.
            return render(request, 'booking/booking_receipt.html', context)
            #return redirect(booking_receipt(request, current_booking, new_form))







        return redirect(index)

    else:
        car = get_object_or_404(Car, id=car_id)
        booking = get_object_or_404(Car_Date_Reservation, id=booking_id)

        number_of_days = (booking.final_date - booking.initial_date).days
        price = price_calculator(number_of_days)


        context = {
            'car': car,
            'booking': booking,
            'days': number_of_days,
            'price': price
        }

        return render(request, 'booking/booking_form.html', context)



def prisTest(request):

    return render(request, 'booking/pristest.html')