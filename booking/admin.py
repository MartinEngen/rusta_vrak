from django.contrib import admin

from . import models
# Register your models here.

class FinalizedBookings(admin.ModelAdmin):
    list_display = ('bil', 'date_made', 'fra_dato', 'til_dato', 'kunde', 'kunde_epost', 'kunde_tlf', 'pris')

    def bil(self, obj):
        return ("%s %s" % (obj.car.brand, obj.car.model)).upper()

    def fra_dato(self, obj):
        return obj.car_date_reservation.initial_date

    def til_dato(self, obj):
        return (obj.car_date_reservation.final_date)

    def kunde(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name))

    def kunde_epost(self, obj):
        return obj.email

    def kunde_tlf(self, obj):
        return obj.phone_number



    def pris(self, obj):
        price = obj.car.price
        days = (obj.car_date_reservation.final_date - obj.car_date_reservation.initial_date).days
        total_price = price * days

        return total_price

    #pris.admin_order_field = 'pris'
    fra_dato.admin_order_field = 'car_date_reservation__initial_date'
    til_dato.admin_order_field = 'car_date_reservation__final_date'

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
admin.site.register(models.Reservation)
admin.site.register(models.Customer)