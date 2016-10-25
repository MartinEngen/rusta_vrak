from django.conf.urls import url
from . import views


urlpatterns = [
    #url(r'^(?P<car_id>[0-9]+)/ledighet/$', views.car_availability, name='car_availability'),
    url(r'^reserver/(?P<car_id>[0-9]+)/$', views.booking_schema, name='reservation_schema'),
    url(r'^pristester/$', views.prisTest, name='pristest'),
    url(r'^pdf/(?P<reservation_id>[0-9]+)/$', views.download_pdf, name='pdf'),
]