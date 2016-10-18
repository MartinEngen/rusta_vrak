from django.contrib import admin

# Register your models here.

from . import models



class CarAdmin(admin.ModelAdmin):
    list_display = ('upper_case_name', 'model', 'car_type')

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.brand, obj.model)).upper()

    upper_case_name.short_description = 'Name'



admin.site.register(models.Car, CarAdmin)
#admin.site.register(models.Car_Booking)
#admin.site.register(models.Registration_Scheme)