from django.contrib import admin

from . import models
from .data_functions import price_calculator
# Register your models here.

class FinalizedBookings(admin.ModelAdmin):
    list_display = ('bil', 'date_made', 'fra_dato', 'til_dato', 'kunde', 'kunde_epost', 'kunde_tlf', 'pris')

    def bil(self, obj):
        return ("%s %s" % (obj.car.brand, obj.car.model)).upper()

    def fra_dato(self, obj):
        return obj.dates_reserved.initial_date

    def til_dato(self, obj):
        return (obj.dates_reserved.final_date)

    def kunde(self, obj):
        return ("%s %s" % (obj.customer.first_name, obj.customer.last_name))

    def kunde_epost(self, obj):
        return obj.customer.email

    def kunde_tlf(self, obj):
        return obj.customer.phone_number


    # TODO: Use the price funciton once it is completed..
    def pris(self, obj):

        price = price_calculator((obj.dates_reserved.final_date - obj.dates_reserved.initial_date).days, obj.car.price)


        return price

    #pris.admin_order_field = 'pris'
    fra_dato.admin_order_field = 'dates_reserved__initial_date'
    til_dato.admin_order_field = 'dates_reserved__final_date'

    search_fields = ['car__brand', 'car__model']

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'author_first_name')

    def author_first_name(self, obj):
        return obj.author.first_name

    author_first_name.admin_order_field = 'author__first_name'

"""
class CarAdmin(admin.ModelAdmin):
    list_display = ('upper_case_name', 'model', 'car_type')

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.brand, obj.model)).upper()

    upper_case_name.short_description = 'Name'
"""


admin.site.register(models.Dates_Reserved)
admin.site.register(models.Reservation, FinalizedBookings)
admin.site.register(models.Customer)