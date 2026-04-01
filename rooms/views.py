from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from .models import Room
from .serializers import RoomSerializer
from bookings.models import Booking
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.conf import settings

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name']
    ordering_fields = ['capacity']

class AvailableRoomsView(APIView):
    def get(self, request):
        start = parse_datetime(request.GET.get('start_time'))
        end = parse_datetime(request.GET.get('end_time'))

        if not start or not end:
            return Response({"error": "Invalid datetime"}, status=400)

        booked_rooms = Booking.objects.filter(
            start_time__lt=end,
            end_time__gt=start
        ).values_list('room_id', flat=True)

        available_rooms = Room.objects.exclude(id__in=booked_rooms)

        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)
    
class RoomAvailabilityView(APIView):
    def get(self, request, pk):
        date_str = request.GET.get("date")

        if not date_str:
            return Response({"error": "date is required"}, status=400)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        tz = timezone.get_current_timezone()

        start_hour = 8
        end_hour = 20

        slots = []
        current = datetime.combine(date, time(start_hour, 0))
        current = timezone.make_aware(current, tz)  # 🔥 penting

        while current.time() < time(end_hour, 0):
            slots.append(current)
            current += timedelta(minutes=30)

        start_of_day = timezone.make_aware(
            datetime.combine(date, time.min),
            tz
        )
        end_of_day = start_of_day + timedelta(days=1)

        bookings = Booking.objects.filter(
            room_id=pk,
            start_time__lt=end_of_day,
            end_time__gt=start_of_day
        )

        result = []

        
        for slot in slots:
            print("CURRENT TZ:", timezone.get_current_timezone())
            print("SLOT:", slot)
            print("LOCAL SLOT:", timezone.localtime(slot))
            print("SETTINGS TZ:", settings.TIME_ZONE)
            slot_end = slot + timedelta(minutes=30)

            is_busy = bookings.filter(
                start_time__lt=slot_end,
                end_time__gt=slot
            ).exists()

            result.append({
                "start_time": timezone.localtime(slot).isoformat(),   # ✅ FIX
                "end_time": timezone.localtime(slot_end).isoformat(), # ✅ FIX
                "status": "busy" if is_busy else "free"
            })

        return Response(result)