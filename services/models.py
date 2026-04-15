from django.db import models
from trains.models import Train, Station
from users.models import User


class LiveTrainStatus(models.Model):
    STATUS_CHOICES = [
        ('ON_TIME', 'Running On Time'),
        ('DELAYED', 'Delayed'),
        ('CANCELLED', 'Cancelled'),
        ('ARRIVED', 'Arrived'),
        ('DEPARTED', 'Departed'),
    ]
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='live_statuses')
    journey_date = models.DateField()
    current_station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    delay_minutes = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ON_TIME')
    last_updated = models.DateTimeField(auto_now=True)
    speed_kmph = models.IntegerField(default=0)

    class Meta:
        unique_together = ['train', 'journey_date']

    def __str__(self):
        return f"{self.train.number} on {self.journey_date} — {self.status}"


class TrainStopStatus(models.Model):
    live_status = models.ForeignKey(LiveTrainStatus, on_delete=models.CASCADE, related_name='stop_statuses')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    stop_number = models.IntegerField()
    scheduled_arrival = models.TimeField(null=True, blank=True)
    scheduled_departure = models.TimeField(null=True, blank=True)
    actual_arrival = models.TimeField(null=True, blank=True)
    actual_departure = models.TimeField(null=True, blank=True)
    delay_minutes = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('DEPARTED', 'Departed'), ('AT_STATION', 'At Station'),
        ('UPCOMING', 'Upcoming'), ('SKIPPED', 'Skipped'),
    ], default='UPCOMING')
    platform_number = models.IntegerField(default=1)

    class Meta:
        ordering = ['stop_number']


class TrainAlert(models.Model):
    ALERT_TYPES = [
        ('DELAY', 'Train Delay'),
        ('PLATFORM', 'Platform Change'),
        ('CANCELLATION', 'Train Cancellation'),
        ('CHART', 'Chart Preparation'),
        ('PNR', 'PNR Status Change'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    journey_date = models.DateField()
    pnr = models.CharField(max_length=10, blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    via_sms = models.BooleanField(default=True)
    via_email = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'train', 'journey_date', 'alert_type']

    def __str__(self):
        return f"Alert: {self.user.username} — {self.train.number} on {self.journey_date}"


class CateringVendor(models.Model):
    name = models.CharField(max_length=200)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='vendors')
    cuisine_type = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    is_active = models.BooleanField(default=True)
    min_order = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    delivery_time_minutes = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.name} @ {self.station.code}"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('MEAL', 'Full Meal'), ('SNACK', 'Snacks'), ('BEVERAGE', 'Beverages'),
        ('BREAKFAST', 'Breakfast'), ('DESSERT', 'Desserts'), ('COMBO', 'Combo'),
    ]
    vendor = models.ForeignKey(CateringVendor, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_veg = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    image_emoji = models.CharField(max_length=10, default='🍱')

    def __str__(self):
        return f"{self.name} — ₹{self.price}"


class CateringOrder(models.Model):
    STATUS_CHOICES = [
        ('PLACED', 'Order Placed'), ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'), ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pnr = models.CharField(max_length=10)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    delivery_station = models.ForeignKey(Station, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    coach_number = models.CharField(max_length=5)
    seat_number = models.CharField(max_length=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} for PNR {self.pnr}"


class CateringOrderItem(models.Model):
    order = models.ForeignKey(CateringOrder, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)


class SeasonPass(models.Model):
    PASS_TYPES = [
        ('MONTHLY', 'Monthly'), ('QUARTERLY', 'Quarterly'), ('HALF_YEARLY', 'Half Yearly'),
    ]
    CLASS_CHOICES = [
        ('2S', 'Second Sitting'), ('SL', 'Sleeper'), ('3A', 'Third AC'),
        ('2A', 'Second AC'), ('CC', 'Chair Car'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='season_passes')
    source_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='passes_from')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='passes_to')
    pass_type = models.CharField(max_length=15, choices=PASS_TYPES)
    travel_class = models.CharField(max_length=5, choices=CLASS_CHOICES)
    valid_from = models.DateField()
    valid_until = models.DateField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    pass_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pass {self.pass_number} — {self.user.username}"


class TourPackage(models.Model):
    CATEGORY_CHOICES = [
        ('HERITAGE', 'Heritage'), ('PILGRIMAGE', 'Pilgrimage'), ('HILL_STATION', 'Hill Station'),
        ('BEACH', 'Beach'), ('WILDLIFE', 'Wildlife'), ('SPECIAL', 'Special'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    itinerary = models.TextField()
    duration_nights = models.IntegerField()
    duration_days = models.IntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    inclusions = models.TextField()
    source_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    max_group_size = models.IntegerField(default=20)
    is_active = models.BooleanField(default=True)
    image_emoji = models.CharField(max_length=10, default='🏔️')
    highlights = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price_per_person:
            return int((1 - float(self.price_per_person) / float(self.original_price)) * 100)
        return 0
