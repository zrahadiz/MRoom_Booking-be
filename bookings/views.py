from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()

        user_id = self.request.query_params.get('user')
        date = self.request.query_params.get('date')

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()

            start_of_day = timezone.make_aware(
                datetime.combine(date_obj, datetime.min.time())
            )
            end_of_day = start_of_day + timedelta(days=1)

            queryset = queryset.filter(
                start_time__gte=start_of_day,
                start_time__lt=end_of_day
            )

        return queryset


class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class CheckBookingView(APIView):
    def post(self, request):
        room = request.data.get("room")
        start = request.data.get("start_time")
        end = request.data.get("end_time")

        conflict = Booking.objects.filter(
            room_id=room,
            start_time__lt=end,
            end_time__gt=start
        ).exists()

        return Response({
            "available": not conflict
        })