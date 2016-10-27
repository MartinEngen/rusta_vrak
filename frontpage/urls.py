from django.conf.urls import url
from . import views

urlpatterns = [
    url('^bil/$', views.search_function, name='search_funciton')
]