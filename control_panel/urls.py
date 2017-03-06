from django.conf.urls import url
from . import views

app_name = 'control_panel'
urlpatterns = [
    # Index
    url(r'^$', views.index_control_panel, name='control_panel_index'),

    # No Business dates url: /control_panel/no_reservations
    url(r'^lock_reservations', views.reservation_locks, name='lock_reservations')
]