from rest_framework import serializers
from .models import Booking, Passenger
from trains.models import CoachClass, SeatAvailability, Train, Station

class PassengerSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    berth_display = serializers.CharField(source='get_berth_preference_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Passenger
        fields = ['id','name','age','gender','gender_display','berth_preference','berth_display',
                  'berth_allotted','coach_number','seat_number','status','status_display',
                  'waitlist_number','id_type','id_number','is_senior_citizen']

class BookingCreateSerializer(serializers.Serializer):
    train_number = serializers.CharField()
    coach_class = serializers.CharField()
    journey_date = serializers.DateField()
    boarding_station_code = serializers.CharField()
    destination_station_code = serializers.CharField()
    quota = serializers.ChoiceField(choices=['GN','TK','PT','LD','HH','DF'], default='GN')
    mobile = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    passengers = PassengerSerializer(many=True, required=True)

    def validate_passengers(self, value):
        if not value:
            raise serializers.ValidationError("At least one passenger is required.")
        if len(value) > 6:
            raise serializers.ValidationError("Maximum 6 passengers per booking.")
        return value

    def validate(self, attrs):
        try:
            train = Train.objects.get(number=attrs['train_number'])
        except Train.DoesNotExist:
            raise serializers.ValidationError({"train_number": "Train not found."})

        try:
            coach_class = CoachClass.objects.get(train=train, coach_class=attrs['coach_class'])
        except CoachClass.DoesNotExist:
            raise serializers.ValidationError({"coach_class": "Class not available on this train."})

        try:
            boarding = Station.objects.get(code=attrs['boarding_station_code'])
            destination = Station.objects.get(code=attrs['destination_station_code'])
        except Station.DoesNotExist:
            raise serializers.ValidationError("Invalid station code.")

        # Check availability
        avail, _ = SeatAvailability.objects.get_or_create(
            coach_class=coach_class, journey_date=attrs['journey_date'],
            defaults={'available_seats': coach_class.total_seats, 'waitlist_count': 0}
        )
        num_passengers = len(attrs['passengers'])
        if avail.available_seats == 0 and avail.waitlist_count >= 100:
            raise serializers.ValidationError("No seats available. Waitlist is full.")

        # Fare calculation
        base_fare = float(coach_class.tatkal_fare if attrs['quota'] == 'TK' else coach_class.base_fare)
        reservation_charge = 40
        gst = base_fare * 0.05
        fare_per_pax = base_fare + reservation_charge + gst
        total_fare = round(fare_per_pax * num_passengers, 2)

        attrs['_train'] = train
        attrs['_coach_class'] = coach_class
        attrs['_boarding'] = boarding
        attrs['_destination'] = destination
        attrs['_avail'] = avail
        attrs['_total_fare'] = total_fare
        return attrs

class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, read_only=True)
    train_number = serializers.CharField(source='train.number', read_only=True)
    train_name = serializers.CharField(source='train.name', read_only=True)
    departure_time = serializers.TimeField(source='train.departure_time', read_only=True)
    arrival_time = serializers.TimeField(source='train.arrival_time', read_only=True)
    coach_class_display = serializers.CharField(source='coach_class.get_coach_class_display', read_only=True)
    boarding_station_code = serializers.CharField(source='boarding_station.code', read_only=True)
    boarding_station_name = serializers.CharField(source='boarding_station.name', read_only=True)
    destination_station_code = serializers.CharField(source='destination_station.code', read_only=True)
    destination_station_name = serializers.CharField(source='destination_station.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    quota_display = serializers.CharField(source='get_quota_display', read_only=True)

    class Meta:
        model = Booking
        fields = ['id','pnr','train_number','train_name','departure_time','arrival_time',
                  'coach_class','coach_class_display','journey_date','boarding_station_code',
                  'boarding_station_name','destination_station_code','destination_station_name',
                  'status','status_display','quota','quota_display','total_fare','booking_date',
                  'is_paid','mobile','email','passengers','chart_prepared']

class PNRStatusSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, read_only=True)
    train_number = serializers.CharField(source='train.number', read_only=True)
    train_name = serializers.CharField(source='train.name', read_only=True)
    train_type = serializers.CharField(source='train.get_train_type_display', read_only=True)
    departure_time = serializers.TimeField(source='train.departure_time', read_only=True)
    arrival_time = serializers.TimeField(source='train.arrival_time', read_only=True)
    coach_class_display = serializers.CharField(source='coach_class.get_coach_class_display', read_only=True)
    boarding_station_code = serializers.CharField(source='boarding_station.code', read_only=True)
    boarding_station_name = serializers.CharField(source='boarding_station.name', read_only=True)
    destination_station_code = serializers.CharField(source='destination_station.code', read_only=True)
    destination_station_name = serializers.CharField(source='destination_station.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = ['pnr','train_number','train_name','train_type','departure_time','arrival_time',
                  'coach_class','coach_class_display','journey_date','boarding_station_code',
                  'boarding_station_name','destination_station_code','destination_station_name',
                  'status','status_display','total_fare','booking_date','chart_prepared','passengers']
