from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.utils import timezone
import random, string
from .models import Booking, Passenger
from .serializers import BookingCreateSerializer, BookingSerializer, PNRStatusSerializer
from trains.models import SeatAvailability

class BookTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        train = data['_train']
        coach_class = data['_coach_class']
        avail = data['_avail']
        passengers_data = data['passengers']
        num_passengers = len(passengers_data)

        # Determine booking status
        booking_status = 'CNF'
        if avail.available_seats >= num_passengers:
            avail.available_seats -= num_passengers
        elif avail.available_seats > 0:
            # Partial confirmed
            avail.waitlist_count += (num_passengers - avail.available_seats)
            avail.available_seats = 0
            booking_status = 'WL'
        else:
            avail.waitlist_count += num_passengers
            booking_status = 'WL'
        avail.save()

        booking = Booking.objects.create(
            user=request.user,
            train=train,
            coach_class=coach_class,
            journey_date=data['journey_date'],
            boarding_station=data['_boarding'],
            destination_station=data['_destination'],
            status=booking_status,
            quota=data['quota'],
            total_fare=data['_total_fare'],
            mobile=data['mobile'],
            email=data['email'],
            is_paid=True,
            payment_id=f"PAY{''.join(random.choices(string.ascii_uppercase+string.digits,k=12))}"
        )

        coaches = ['S1','S2','S3','S4','B1','B2','A1','A2']
        for i, pax_data in enumerate(passengers_data):
            pax_status = 'CNF' if booking_status == 'CNF' else 'WL'
            coach = random.choice(coaches)
            seat = random.randint(1, 72)
            berths = ['LB','MB','UB','SL','SU']
            Passenger.objects.create(
                booking=booking,
                name=pax_data['name'],
                age=pax_data['age'],
                gender=pax_data['gender'],
                berth_preference=pax_data.get('berth_preference','NP'),
                berth_allotted=random.choice(berths) if pax_status == 'CNF' else '',
                coach_number=coach if pax_status == 'CNF' else '',
                seat_number=str(seat) if pax_status == 'CNF' else '',
                status=pax_status,
                waitlist_number=avail.waitlist_count - num_passengers + i + 1 if pax_status == 'WL' else None,
                id_type=pax_data.get('id_type',''),
                id_number=pax_data.get('id_number',''),
                is_senior_citizen=pax_data['age'] >= 60
            )

        return Response({
            'message': 'Booking successful',
            'booking': BookingSerializer(booking).data
        }, status=status.HTTP_201_CREATED)

class PNRStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pnr):
        try:
            booking = Booking.objects.select_related(
                'train','coach_class','boarding_station','destination_station'
            ).prefetch_related('passengers').get(pnr=pnr)
        except Booking.DoesNotExist:
            return Response({'error': 'PNR not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PNRStatusSerializer(booking).data)

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Booking.objects.filter(user=self.request.user).select_related(
            'train','coach_class','boarding_station','destination_station'
        ).prefetch_related('passengers').order_by('-booking_date')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            'train','coach_class','boarding_station','destination_station'
        ).prefetch_related('passengers')

class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == 'CAN':
            return Response({'error': 'Booking already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.chart_prepared:
            return Response({'error': 'Cannot cancel after chart preparation'}, status=status.HTTP_400_BAD_REQUEST)

        refund = booking.calculate_refund()
        booking.status = 'CAN'
        booking.cancellation_date = timezone.now()
        booking.refund_amount = refund
        booking.save()

        # Release seats
        try:
            avail = SeatAvailability.objects.get(
                coach_class=booking.coach_class, journey_date=booking.journey_date
            )
            confirmed_pax = booking.passengers.filter(status='CNF').count()
            avail.available_seats += confirmed_pax
            avail.save()
        except SeatAvailability.DoesNotExist:
            pass

        booking.passengers.all().update(status='CAN')

        return Response({
            'message': 'Booking cancelled successfully',
            'pnr': booking.pnr,
            'refund_amount': refund,
            'refund_info': 'Refund will be credited within 5-7 business days'
        })
