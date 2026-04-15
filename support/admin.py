from django.contrib import admin
from .models import SupportTicket, TicketReply, FAQ

class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'name', 'category', 'priority', 'status', 'created_at']
    list_filter = ['category', 'priority', 'status']
    search_fields = ['ticket_id', 'name', 'email', 'pnr']
    inlines = [TicketReplyInline]
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'section', 'order', 'is_active']
    list_filter = ['section', 'is_active']
    list_editable = ['order', 'is_active']
