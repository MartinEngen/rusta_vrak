from django.contrib import admin

# Register your models here.

from . import models



class CarImagesInline(admin.TabularInline):
    model = models.CarImages

class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'upper_case_name', 'model', 'license_plate' ,'car_type')

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.brand, obj.model)).upper()

    upper_case_name.short_description = 'Name'

    search_fields = ['brand', 'model', 'license_plate', 'car_type']

    inlines = [
        CarImagesInline,
    ]



admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarImages)
#admin.site.register(models.Car_Booking)
#admin.site.register(models.Registration_Scheme)