from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import date, datetime
import random, string
from .models import (LiveTrainStatus, TrainStopStatus, TrainAlert,
                     CateringVendor, MenuItem, CateringOrder, CateringOrderItem,
                     SeasonPass, TourPackage)
from .serializers import (LiveTrainStatusSerializer, TrainAlertSerializer,
                           TrainAlertCreateSerializer, CateringVendorSerializer,
                           CateringOrderSerializer, CateringOrderCreateSerializer,
                           SeasonPassSerializer, TourPackageSerializer)
from trains.models import Train, Station


class LiveTrainStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, train_number):
        journey_date_str = request.query_params.get('date', str(date.today()))
        try:
            journey_date = date.fromisoformat(journey_date_str)
        except ValueError:
            return Response({'error': 'Invalid date. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            train = Train.objects.get(number=train_number)
        except Train.DoesNotExist:
            return Response({'error': 'Train not found'}, status=status.HTTP_404_NOT_FOUND)

        live, created = LiveTrainStatus.objects.get_or_create(
            train=train, journey_date=journey_date,
            defaults={
                'delay_minutes': random.choice([0, 0, 0, 5, 10, 15, 20, 30]),
                'status': random.choice(['ON_TIME', 'ON_TIME', 'ON_TIME', 'DELAYED']),
                'speed_kmph': random.randint(60, 110),
            }
        )
        serializer = LiveTrainStatusSerializer(live)
        return Response(serializer.data)


class PlatformInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        station_code = request.query_params.get('station')
        if not station_code:
            return Response({'error': 'station parameter required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            station = Station.objects.get(code__iexact=station_code)
        except Station.DoesNotExist:
            return Response({'error': 'Station not found'}, status=status.HTTP_404_NOT_FOUND)

        arriving_trains = Train.objects.filter(destination_station=station).select_related(
            'source_station', 'destination_station')[:6]
        departing_trains = Train.objects.filter(source_station=station).select_related(
            'source_station', 'destination_station')[:6]

        platforms = []
        for i, t in enumerate(list(departing_trains) + list(arriving_trains), 1):
            delay = random.choice([0, 0, 0, 5, 10, 20])
            platforms.append({
                'platform': i,
                'train_number': t.number,
                'train_name': t.name,
                'type': 'Departure' if t.source_station == station else 'Arrival',
                'scheduled_time': str(t.departure_time if t.source_station == station else t.arrival_time),
                'delay_minutes': delay,
                'status': 'On Time' if delay == 0 else f'Delayed by {delay} min',
                'from': t.source_station.city,
                'to': t.destination_station.city,
            })

        return Response({
            'station_code': station.code,
            'station_name': station.name,
            'city': station.city,
            'platforms': platforms
        })


class TrainAlertListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        alerts = TrainAlert.objects.filter(user=request.user, is_active=True)
        return Response(TrainAlertSerializer(alerts, many=True).data)

    def post(self, request):
        ser = TrainAlertCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        try:
            train = Train.objects.get(number=data['train_number'])
        except Train.DoesNotExist:
            return Response({'error': 'Train not found'}, status=status.HTTP_404_NOT_FOUND)

        created_alerts = []
        for alert_type in data['alert_types']:
            alert, _ = TrainAlert.objects.get_or_create(
                user=request.user, train=train,
                journey_date=data['journey_date'], alert_type=alert_type,
                defaults={
                    'pnr': data.get('pnr', ''),
                    'via_sms': data['via_sms'],
                    'via_email': data['via_email'],
                    'is_active': True,
                }
            )
            created_alerts.append(alert)

        return Response({
            'message': f'{len(created_alerts)} alert(s) set successfully',
            'alerts': TrainAlertSerializer(created_alerts, many=True).data
        }, status=status.HTTP_201_CREATED)


class TrainAlertDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            alert = TrainAlert.objects.get(pk=pk, user=request.user)
            alert.delete()
            return Response({'message': 'Alert removed'})
        except TrainAlert.DoesNotExist:
            return Response({'error': 'Alert not found'}, status=status.HTTP_404_NOT_FOUND)


class CateringMenuView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        station_code = request.query_params.get('station')
        category = request.query_params.get('category', '')
        veg_only = request.query_params.get('veg', 'false').lower() == 'true'

        vendors = CateringVendor.objects.filter(is_active=True)
        if station_code:
            vendors = vendors.filter(station__code__iexact=station_code)
        vendors = vendors.select_related('station').prefetch_related('menu_items')

        return Response(CateringVendorSerializer(vendors, many=True).data)


class CateringOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = CateringOrder.objects.filter(user=request.user).order_by('-created_at')
        return Response(CateringOrderSerializer(orders, many=True).data)

    def post(self, request):
        ser = CateringOrderCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        try:
            train = Train.objects.get(number=data['train_number'])
            station = Station.objects.get(code=data['delivery_station_code'])
        except (Train.DoesNotExist, Station.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        order_id = 'CAT' + ''.join(random.choices(string.digits, k=10))
        total = 0
        order_items = []
        for item_data in data['items']:
            try:
                menu_item = MenuItem.objects.get(pk=item_data['menu_item_id'], is_available=True)
                qty = int(item_data['quantity'])
                total += float(menu_item.price) * qty
                order_items.append((menu_item, qty))
            except MenuItem.DoesNotExist:
                return Response({'error': f"Menu item {item_data['menu_item_id']} not found"},
                                status=status.HTTP_404_NOT_FOUND)

        order = CateringOrder.objects.create(
            user=request.user, pnr=data['pnr'], train=train,
            delivery_station=station, delivery_date=data['delivery_date'],
            coach_number=data['coach_number'], seat_number=data['seat_number'],
            total_amount=round(total, 2), order_id=order_id
        )
        for menu_item, qty in order_items:
            CateringOrderItem.objects.create(
                order=order, menu_item=menu_item,
                quantity=qty, unit_price=menu_item.price
            )

        return Response({
            'message': 'Order placed successfully',
            'order': CateringOrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class SeasonPassListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    PASS_FARES = {
        ('MONTHLY', '2S'): 250, ('MONTHLY', 'SL'): 380, ('MONTHLY', 'CC'): 420,
        ('MONTHLY', '3A'): 680, ('MONTHLY', '2A'): 950,
        ('QUARTERLY', '2S'): 650, ('QUARTERLY', 'SL'): 980, ('QUARTERLY', 'CC'): 1100,
        ('QUARTERLY', '3A'): 1800, ('QUARTERLY', '2A'): 2500,
        ('HALF_YEARLY', '2S'): 1100, ('HALF_YEARLY', 'SL'): 1700,
        ('HALF_YEARLY', 'CC'): 1900, ('HALF_YEARLY', '3A'): 3100,
        ('HALF_YEARLY', '2A'): 4200,
    }

    def get(self, request):
        passes = SeasonPass.objects.filter(user=request.user).order_by('-created_at')
        return Response(SeasonPassSerializer(passes, many=True).data)

    def post(self, request):
        src_code = request.data.get('source_station_code')
        dst_code = request.data.get('destination_station_code')
        pass_type = request.data.get('pass_type')
        travel_class = request.data.get('travel_class')
        valid_from_str = request.data.get('valid_from')

        if not all([src_code, dst_code, pass_type, travel_class, valid_from_str]):
            return Response({'error': 'All fields required: source_station_code, destination_station_code, pass_type, travel_class, valid_from'},
                           status=status.HTTP_400_BAD_REQUEST)

        try:
            src = Station.objects.get(code=src_code)
            dst = Station.objects.get(code=dst_code)
            valid_from = date.fromisoformat(valid_from_str)
        except (Station.DoesNotExist, ValueError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        from datetime import timedelta
        duration_map = {'MONTHLY': 30, 'QUARTERLY': 90, 'HALF_YEARLY': 180}
        valid_until = valid_from + timedelta(days=duration_map.get(pass_type, 30))
        amount = self.PASS_FARES.get((pass_type, travel_class), 500)
        pass_number = 'SP' + ''.join(random.choices(string.digits, k=10))

        sp = SeasonPass.objects.create(
            user=request.user, source_station=src, destination_station=dst,
            pass_type=pass_type, travel_class=travel_class,
            valid_from=valid_from, valid_until=valid_until,
            amount_paid=amount, pass_number=pass_number
        )
        return Response({
            'message': 'Season pass issued successfully',
            'pass': SeasonPassSerializer(sp).data
        }, status=status.HTTP_201_CREATED)


class TourPackageListView(generics.ListAPIView):
    serializer_class = TourPackageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = TourPackage.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        max_price = self.request.query_params.get('max_price')
        if category:
            qs = qs.filter(category=category)
        if max_price:
            qs = qs.filter(price_per_person__lte=max_price)
        return qs


class TourPackageDetailView(generics.RetrieveAPIView):
    queryset = TourPackage.objects.filter(is_active=True)
    serializer_class = TourPackageSerializer
    permission_classes = [permissions.AllowAny]
