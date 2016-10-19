from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from cars.models import Car
from booking.models import Car_Date_Reservation, Registration_Schema
from .forms import SearchForm


def index(request):

    """
    context = {
        'personal_cars': '',
        'van': '',
        'combi_car': '',
    }
    """

    return render(request, 'frontpage/index.html')



def search_funciton(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            print('Valid search form, lets do some queries.')

            inital_date = search_form.cleaned_data['initial_date']
            final_date = search_form.cleaned_data['final_date']

            searched_types = []
            if search_form.cleaned_data['personal']:
                searched_types.append(1)
            if search_form.cleaned_data['van']:
                searched_types.append(2)
            if search_form.cleaned_data['combi_car']:
                searched_types.append(3)


            # All cars of wanted Car Type
            cars = Car.objects.filter(car_type__in=searched_types)

            # All bookings of current cars
            car_bookings = Registration_Schema.objects.filter(car__in=cars)


            # Overlapping by final date
            final_date_booking_overlap = car_bookings.filter(car_date_reservation__final_date__range=(inital_date, final_date))
            # Overlapping by inital date
            initial_date_booking_overlap = car_bookings.filter(car_date_reservation__initial_date__range=(inital_date, final_date))
            # Remove the cars with overlapping dates
            cars = cars.exclude(reserved_car__booking__car__in=final_date_booking_overlap.values("car")).exclude(reserved_car__booking__car__in=initial_date_booking_overlap.values("car"))


            context = {
                'cars': cars
            }
            return render(request, 'cars/car_list.html', context)

        else:
            return redirect('/')

    else:
        return redirect('/')
