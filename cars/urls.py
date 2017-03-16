from django.conf.urls import url
from . import views

app_name = 'cars'
urlpatterns = [
    url(r'^biler/$', views.car_list, name='car_list'),
    url(r'^bil/(?P<car_id>[0-9]+)/$', views.specific_car, name='car_availability'),
]
