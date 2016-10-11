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

            # Gather all the cars with the correct car type.
            cars = Car.objects.filter(car_type__in=searched_types)

            # Exclude any cars with initial date greater than final date searched.
            car_bookings = Car_Booking.objects.filter(car=cars)
            print(car_bookings.values("car_id"))
            the_cars = car_bookings.values("car_id")
            print(the_cars)
            print(car_bookings.count())
            car_bookings = car_bookings.exclude(final_date__range=(inital_date, final_date))
            print(car_bookings.count())
            car_bookings = car_bookings.exclude(initial_date__range=(inital_date, final_date))
            print(car_bookings.count())
            cars = cars.filter(booking__booking__car_id__in=car_bookings.values("car_id"))


            print(car_bookings.values("car_id"))
            # List containing all avalable cars
            available = []

            for car in car_bookings:
                print("Adding car. + " + str(car.car))
                available.append(car.car)


            context = {
                'cars': cars
            }
            return render(request, 'cars/search_cars.html', context)

        else:
            return redirect('/')

    else:
        return redirect('/')
