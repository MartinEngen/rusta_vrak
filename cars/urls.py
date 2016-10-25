from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^biler/$', views.car_list, name='car_list'),
    url(r'^bil/(?P<car_id>[0-9]+)/$', views.specific_car, name='car_availability'),
    #url(r'^booking/(?P<car_id>[0-9]+)/(?P<booking_id>[0-9]+)/$', views.booking_schema, name='booking_scheme'),
    #url(r'^booking/kvitering/(?P<registration_id>[0-9]+)/(?P<booking_id>[0-9]+)/$', views.booking_receipt, name='booking_receipt')
]