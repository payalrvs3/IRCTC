from rest_framework import serializers
from .models import SupportTicket, TicketReply, FAQ


class TicketReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = ['id', 'sender', 'is_staff', 'message', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    replies = TicketReplySerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SupportTicket
        fields = ['ticket_id', 'name', 'email', 'mobile', 'pnr',
                  'category', 'category_display', 'priority', 'priority_display',
                  'subject', 'description', 'status', 'status_display',
                  'created_at', 'updated_at', 'replies']


class SupportTicketCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=15, required=False, allow_blank=True)
    pnr = serializers.CharField(max_length=10, required=False, allow_blank=True)
    category = serializers.ChoiceField(choices=[
        'BOOKING', 'REFUND', 'PNR', 'CATERING', 'PAYMENT', 'ACCOUNT', 'DELAY', 'OTHER'])
    priority = serializers.ChoiceField(choices=['NORMAL', 'URGENT', 'CRITICAL'], default='NORMAL')
    subject = serializers.CharField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField()


class FAQSerializer(serializers.ModelSerializer):
    section_display = serializers.CharField(source='get_section_display', read_only=True)

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'section', 'section_display']
