from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from cars.models import Car
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

        return render(request, 'cars/search_cars.html')

    else:

        return render(request, 'frontpage/index.html')