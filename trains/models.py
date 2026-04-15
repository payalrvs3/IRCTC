from django.db import models

class Station(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zone = models.CharField(max_length=50, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Train(models.Model):
    TRAIN_TYPES = [
        ('RAJ','Rajdhani'),('SHT','Shatabdi'),('DUR','Duronto'),
        ('EXP','Express'),('MAIL','Mail'),('PAS','Passenger'),
        ('SF','Superfast'),('ICE','InterCity Express'),
    ]
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    train_type = models.CharField(max_length=10, choices=TRAIN_TYPES)
    source_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departing_trains')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arriving_trains')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration_minutes = models.IntegerField()
    distance_km = models.IntegerField(default=0)
    runs_on_mon = models.BooleanField(default=True)
    runs_on_tue = models.BooleanField(default=True)
    runs_on_wed = models.BooleanField(default=True)
    runs_on_thu = models.BooleanField(default=True)
    runs_on_fri = models.BooleanField(default=True)
    runs_on_sat = models.BooleanField(default=True)
    runs_on_sun = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    pantry_car = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number} - {self.name}"

    @property
    def running_days(self):
        days = []
        if self.runs_on_mon: days.append('Mon')
        if self.runs_on_tue: days.append('Tue')
        if self.runs_on_wed: days.append('Wed')
        if self.runs_on_thu: days.append('Thu')
        if self.runs_on_fri: days.append('Fri')
        if self.runs_on_sat: days.append('Sat')
        if self.runs_on_sun: days.append('Sun')
        return days

    @property
    def duration_display(self):
        h, m = divmod(self.duration_minutes, 60)
        return f"{h}h {m:02d}m"

class TrainStop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='stops')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    stop_number = models.IntegerField()
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    distance_from_source = models.IntegerField(default=0)
    halt_minutes = models.IntegerField(default=2)
    platform_number = models.IntegerField(default=1)

    class Meta:
        ordering = ['stop_number']
        unique_together = ['train', 'stop_number']

    def __str__(self):
        return f"{self.train.number} - Stop {self.stop_number}: {self.station.code}"

class CoachClass(models.Model):
    CLASS_CHOICES = [
        ('1A','First AC'),('2A','Second AC'),('3A','Third AC'),
        ('SL','Sleeper'),('CC','Chair Car'),('2S','Second Sitting'),
        ('GN','General'),('FC','First Class'),
    ]
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='coach_classes')
    coach_class = models.CharField(max_length=5, choices=CLASS_CHOICES)
    total_seats = models.IntegerField()
    base_fare = models.DecimalField(max_digits=8, decimal_places=2)
    tatkal_fare = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    coach_count = models.IntegerField(default=1)

    class Meta:
        unique_together = ['train', 'coach_class']

    def __str__(self):
        return f"{self.train.number} - {self.coach_class}"

class SeatAvailability(models.Model):
    coach_class = models.ForeignKey(CoachClass, on_delete=models.CASCADE, related_name='availability')
    journey_date = models.DateField()
    available_seats = models.IntegerField()
    waitlist_count = models.IntegerField(default=0)
    rac_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['coach_class', 'journey_date']

    @property
    def status(self):
        if self.available_seats > 0:
            return f"AVBL {self.available_seats}"
        elif self.rac_count > 0:
            return f"RAC {self.rac_count}"
        else:
            return f"WL {self.waitlist_count}"
