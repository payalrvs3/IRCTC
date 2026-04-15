from django.contrib import admin
from .models import Station, Train, TrainStop, CoachClass, SeatAvailability

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['code','name','city','state','zone']
    search_fields = ['code','name','city']
    list_filter = ['state','zone']

class TrainStopInline(admin.TabularInline):
    model = TrainStop
    extra = 0

class CoachClassInline(admin.TabularInline):
    model = CoachClass
    extra = 0

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['number','name','train_type','source_station','destination_station','departure_time','is_active']
    search_fields = ['number','name']
    list_filter = ['train_type','is_active']
    inlines = [CoachClassInline, TrainStopInline]

@admin.register(SeatAvailability)
class SeatAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['coach_class','journey_date','available_seats','waitlist_count']
    list_filter = ['journey_date']
