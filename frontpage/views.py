from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from cars.models import Car, Car_Booking
from .forms import SearchForm


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")

    if request.method == 'POST':

        search = SearchForm(request.POST)

        if search.is_valid():
            print("Valid Search :))")
            print(search.cleaned_data['personal'])
            print(search.cleaned_data['van'])
            print(search.cleaned_data['combi_car'])






        return render(request, 'frontpage/index.html')
    else:

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
        print('Posted info')

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

            print(searched_types)
            # Gather all the cars with the correct car type. car__car_type__in=searched_types
            #available_cars = Car_Booking.objects.filter(car__car_type=1)
            cars = Car.objects.filter(car_type__in=searched_types)
            print(cars)
            # Exclude any cars with initial date greater than final date searched.
            available_cars = Car_Booking.objects.filter(car=cars)
            available_cars = available_cars.exclude(final_date__lte=final_date)
            available_cars = available_cars.exclude(initial_date__gte=inital_date)


            available = []

            for car in available_cars:
                print("Adding car. + " + str(car.car))
                available.append(car.car)
            #available_cars = available_cars.exclude(final_date__gt=inital_date)
            #available_cars = available_cars.exclude(initial_date__lt=final_date)





            print available

        return render(request, 'cars/search_cars.html')

    else:

        return render(request, 'frontpage/index.html')