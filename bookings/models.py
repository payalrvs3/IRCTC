import random, string
from django.db import models
from users.models import User
from trains.models import Train, CoachClass, SeatAvailability

def generate_pnr():
    return ''.join(random.choices(string.digits, k=10))

class Booking(models.Model):
    STATUS_CHOICES = [
        ('CNF','Confirmed'),('WL','Waitlisted'),('RAC','RAC'),
        ('CAN','Cancelled'),('PCAN','Partially Cancelled'),
    ]
    QUOTA_CHOICES = [
        ('GN','General'),('TK','Tatkal'),('PT','Premium Tatkal'),
        ('LD','Ladies'),('HH','Physically Handicapped'),('DF','Defence'),
    ]

    pnr = models.CharField(max_length=10, unique=True, default=generate_pnr)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    coach_class = models.ForeignKey(CoachClass, on_delete=models.CASCADE)
    journey_date = models.DateField()
    boarding_station = models.ForeignKey('trains.Station', on_delete=models.CASCADE, related_name='boarding_bookings')
    destination_station = models.ForeignKey('trains.Station', on_delete=models.CASCADE, related_name='destination_bookings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CNF')
    quota = models.CharField(max_length=5, choices=QUOTA_CHOICES, default='GN')
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    chart_prepared = models.BooleanField(default=False)

    def __str__(self):
        return f"PNR: {self.pnr} | {self.train.number} | {self.journey_date}"

    def calculate_refund(self):
        from datetime import datetime, timezone
        journey_dt = datetime.combine(self.journey_date, self.train.departure_time)
        now = datetime.now()
        hours_to_departure = (journey_dt - now).total_seconds() / 3600
        fare = float(self.total_fare)
        if hours_to_departure > 48:
            return fare * 0.75
        elif hours_to_departure > 12:
            return fare * 0.50
        elif hours_to_departure > 4:
            return fare * 0.25
        return 0

class Passenger(models.Model):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]
    BERTH_CHOICES = [('LB','Lower'),('MB','Middle'),('UB','Upper'),('SL','Side Lower'),('SU','Side Upper'),('NP','No Preference')]
    STATUS_CHOICES = [('CNF','Confirmed'),('WL','Waitlisted'),('RAC','RAC'),('CAN','Cancelled')]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    berth_preference = models.CharField(max_length=5, choices=BERTH_CHOICES, default='NP')
    berth_allotted = models.CharField(max_length=5, blank=True)
    coach_number = models.CharField(max_length=5, blank=True)
    seat_number = models.CharField(max_length=5, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CNF')
    waitlist_number = models.IntegerField(null=True, blank=True)
    id_type = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    is_senior_citizen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.booking.pnr})"
