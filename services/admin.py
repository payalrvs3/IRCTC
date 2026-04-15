from django.contrib import admin
from .models import (LiveTrainStatus, TrainAlert, CateringVendor, MenuItem,
                     CateringOrder, SeasonPass, TourPackage)

@admin.register(LiveTrainStatus)
class LiveTrainStatusAdmin(admin.ModelAdmin):
    list_display = ['train', 'journey_date', 'status', 'delay_minutes', 'last_updated']
    list_filter = ['status', 'journey_date']

@admin.register(TrainAlert)
class TrainAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'train', 'journey_date', 'alert_type', 'is_active']
    list_filter = ['alert_type', 'is_active']

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0

@admin.register(CateringVendor)
class CateringVendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'station', 'cuisine_type', 'rating', 'is_active']
    inlines = [MenuItemInline]

@admin.register(CateringOrder)
class CateringOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'pnr', 'train', 'status', 'total_amount', 'created_at']
    list_filter = ['status']

@admin.register(SeasonPass)
class SeasonPassAdmin(admin.ModelAdmin):
    list_display = ['pass_number', 'user', 'source_station', 'destination_station', 'pass_type', 'valid_until']

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'duration_days', 'price_per_person', 'is_active']
    list_filter = ['category', 'is_active']
