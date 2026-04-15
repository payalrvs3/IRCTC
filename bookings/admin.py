from django.contrib import admin
from .models import Booking, Passenger

class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0
    readonly_fields = ['coach_number','seat_number','berth_allotted','status']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['pnr','user','train','journey_date','status','total_fare','booking_date']
    search_fields = ['pnr','user__username','train__number']
    list_filter = ['status','quota','journey_date']
    inlines = [PassengerInline]
    readonly_fields = ['pnr','booking_date','payment_id']
