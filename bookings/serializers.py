from rest_framework import serializers
from django.utils import timezone
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        start = data['start_time']
        end = data['end_time']
        room = data['room']

        if end <= start:
            raise serializers.ValidationError(
                "end_time must be greater than start_time"
            )

        if start < timezone.now():
            raise serializers.ValidationError(
                "Booking cannot be in the past"
            )

        conflicts = Booking.objects.filter(
            room=room,
            start_time__lt=end,
            end_time__gt=start
        )

        if conflicts.exists():
            raise serializers.ValidationError(
                "Room already booked for this time"
            )

        return data