from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from cars.models import Car


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")

    """
    context = {
        'personal_cars': '',
        'van': '',
        'combi_car': '',
    }
    """

    return render(request, 'frontpage/index.html')
