from rest_framework import serializers
from .models import Car_Booking

class Car_BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car_Booking
        fields = ('initial_date', 'final_date')