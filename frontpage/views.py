from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from cars.models import Car, Car_Booking
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
            car_bookings = Car_Booking.objects.filter(car__in=cars)


            # Overlapping by final date
            final_date_booking_overlap = car_bookings.filter(final_date__range=(inital_date, final_date))

            # Overlapping by inital date
            initial_date_booking_overlap = car_bookings.filter(initial_date__range=(inital_date, final_date))

            # Remove the cars with overlapping dates
            cars = cars.exclude(booking__booking__car__in=final_date_booking_overlap.values("car")).exclude(booking__booking__car__in=initial_date_booking_overlap.values("car"))


            context = {
                'cars': cars
            }
            return render(request, 'cars/search_cars.html', context)

        else:
            return redirect('/')

    else:
        return redirect('/')
