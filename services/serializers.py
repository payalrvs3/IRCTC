from rest_framework import serializers
from .models import (LiveTrainStatus, TrainStopStatus, TrainAlert,
                     CateringVendor, MenuItem, CateringOrder, CateringOrderItem,
                     SeasonPass, TourPackage)


class TrainStopStatusSerializer(serializers.ModelSerializer):
    station_code = serializers.CharField(source='station.code', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    city = serializers.CharField(source='station.city', read_only=True)

    class Meta:
        model = TrainStopStatus
        fields = ['stop_number', 'station_code', 'station_name', 'city',
                  'scheduled_arrival', 'scheduled_departure',
                  'actual_arrival', 'actual_departure',
                  'delay_minutes', 'status', 'platform_number']


class LiveTrainStatusSerializer(serializers.ModelSerializer):
    train_number = serializers.CharField(source='train.number', read_only=True)
    train_name = serializers.CharField(source='train.name', read_only=True)
    current_station_code = serializers.CharField(source='current_station.code', read_only=True)
    current_station_name = serializers.CharField(source='current_station.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    stop_statuses = TrainStopStatusSerializer(many=True, read_only=True)

    class Meta:
        model = LiveTrainStatus
        fields = ['train_number', 'train_name', 'journey_date',
                  'current_station_code', 'current_station_name',
                  'delay_minutes', 'status', 'status_display',
                  'last_updated', 'speed_kmph', 'stop_statuses']


class TrainAlertSerializer(serializers.ModelSerializer):
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    train_number = serializers.CharField(source='train.number', read_only=True)
    train_name = serializers.CharField(source='train.name', read_only=True)

    class Meta:
        model = TrainAlert
        fields = ['id', 'train_number', 'train_name', 'journey_date', 'pnr',
                  'alert_type', 'alert_type_display', 'via_sms', 'via_email',
                  'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TrainAlertCreateSerializer(serializers.Serializer):
    train_number = serializers.CharField()
    journey_date = serializers.DateField()
    pnr = serializers.CharField(required=False, allow_blank=True)
    alert_types = serializers.ListField(child=serializers.ChoiceField(
        choices=['DELAY', 'PLATFORM', 'CANCELLATION', 'CHART', 'PNR']))
    via_sms = serializers.BooleanField(default=True)
    via_email = serializers.BooleanField(default=True)


class MenuItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'category', 'category_display',
                  'price', 'is_veg', 'is_available', 'image_emoji']


class CateringVendorSerializer(serializers.ModelSerializer):
    station_code = serializers.CharField(source='station.code', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = CateringVendor
        fields = ['id', 'name', 'station_code', 'station_name', 'cuisine_type',
                  'rating', 'min_order', 'delivery_time_minutes', 'menu_items']


class CateringOrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='menu_item.name', read_only=True)
    item_emoji = serializers.CharField(source='menu_item.image_emoji', read_only=True)

    class Meta:
        model = CateringOrderItem
        fields = ['id', 'item_name', 'item_emoji', 'quantity', 'unit_price']


class CateringOrderSerializer(serializers.ModelSerializer):
    items = CateringOrderItemSerializer(many=True, read_only=True)
    train_number = serializers.CharField(source='train.number', read_only=True)
    delivery_station_name = serializers.CharField(source='delivery_station.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CateringOrder
        fields = ['id', 'order_id', 'pnr', 'train_number', 'delivery_station_name',
                  'delivery_date', 'coach_number', 'seat_number',
                  'status', 'status_display', 'total_amount', 'created_at', 'items']


class CateringOrderCreateSerializer(serializers.Serializer):
    pnr = serializers.CharField(max_length=10)
    train_number = serializers.CharField()
    delivery_station_code = serializers.CharField()
    delivery_date = serializers.DateField()
    coach_number = serializers.CharField(max_length=5)
    seat_number = serializers.CharField(max_length=5)
    items = serializers.ListField(child=serializers.DictField())

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        for item in value:
            if 'menu_item_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item needs menu_item_id and quantity.")
        return value


class SeasonPassSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(source='source_station.code', read_only=True)
    source_name = serializers.CharField(source='source_station.name', read_only=True)
    destination_code = serializers.CharField(source='destination_station.code', read_only=True)
    destination_name = serializers.CharField(source='destination_station.name', read_only=True)
    pass_type_display = serializers.CharField(source='get_pass_type_display', read_only=True)
    class_display = serializers.CharField(source='get_travel_class_display', read_only=True)

    class Meta:
        model = SeasonPass
        fields = ['id', 'pass_number', 'source_code', 'source_name',
                  'destination_code', 'destination_name',
                  'pass_type', 'pass_type_display', 'travel_class', 'class_display',
                  'valid_from', 'valid_until', 'amount_paid', 'is_active', 'created_at']


class TourPackageSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = TourPackage
        fields = ['id', 'name', 'category', 'category_display', 'description',
                  'duration_nights', 'duration_days', 'price_per_person',
                  'original_price', 'discount_percent', 'inclusions',
                  'source_city', 'destination_city', 'max_group_size',
                  'image_emoji', 'highlights']
