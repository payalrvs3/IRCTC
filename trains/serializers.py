from rest_framework import serializers
from .models import Station, Train, TrainStop, CoachClass, SeatAvailability

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class TrainStopSerializer(serializers.ModelSerializer):
    station_code = serializers.CharField(source='station.code', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    city = serializers.CharField(source='station.city', read_only=True)

    class Meta:
        model = TrainStop
        fields = ['stop_number','station_code','station_name','city','arrival_time','departure_time',
                  'distance_from_source','halt_minutes','platform_number']

class SeatAvailabilitySerializer(serializers.ModelSerializer):
    coach_class = serializers.CharField(source='coach_class.coach_class', read_only=True)
    coach_class_display = serializers.CharField(source='coach_class.get_coach_class_display', read_only=True)
    base_fare = serializers.DecimalField(source='coach_class.base_fare', max_digits=8, decimal_places=2, read_only=True)
    tatkal_fare = serializers.DecimalField(source='coach_class.tatkal_fare', max_digits=8, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = SeatAvailability
        fields = ['coach_class','coach_class_display','available_seats','waitlist_count','rac_count','base_fare','tatkal_fare','status']

class CoachClassSerializer(serializers.ModelSerializer):
    coach_class_display = serializers.CharField(source='get_coach_class_display', read_only=True)

    class Meta:
        model = CoachClass
        fields = ['coach_class','coach_class_display','total_seats','base_fare','tatkal_fare','coach_count']

class TrainListSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(source='source_station.code', read_only=True)
    source_name = serializers.CharField(source='source_station.name', read_only=True)
    destination_code = serializers.CharField(source='destination_station.code', read_only=True)
    destination_name = serializers.CharField(source='destination_station.name', read_only=True)
    train_type_display = serializers.CharField(source='get_train_type_display', read_only=True)
    duration_display = serializers.CharField(read_only=True)
    running_days = serializers.ListField(read_only=True)
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Train
        fields = ['id','number','name','train_type','train_type_display','source_code','source_name',
                  'destination_code','destination_name','departure_time','arrival_time','duration_display',
                  'distance_km','running_days','pantry_car','availability']

    def get_availability(self, obj):
        journey_date = self.context.get('journey_date')
        if not journey_date:
            return []
        avail = SeatAvailability.objects.filter(
            coach_class__train=obj, journey_date=journey_date
        ).select_related('coach_class')
        return SeatAvailabilitySerializer(avail, many=True).data

class TrainDetailSerializer(TrainListSerializer):
    stops = TrainStopSerializer(many=True, read_only=True)
    coach_classes = CoachClassSerializer(many=True, read_only=True)

    class Meta(TrainListSerializer.Meta):
        fields = TrainListSerializer.Meta.fields + ['stops','coach_classes']
