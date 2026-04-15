from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import SupportTicket, TicketReply, FAQ
from .serializers import (SupportTicketSerializer, SupportTicketCreateSerializer,
                           TicketReplySerializer, FAQSerializer)


class SubmitTicketView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = SupportTicketCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        ticket = SupportTicket.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=data['name'],
            email=data['email'],
            mobile=data.get('mobile', ''),
            pnr=data.get('pnr', ''),
            category=data['category'],
            priority=data.get('priority', 'NORMAL'),
            subject=data.get('subject', ''),
            description=data['description'],
        )
        return Response({
            'message': 'Support ticket submitted successfully',
            'ticket_id': ticket.ticket_id,
            'status': ticket.status,
            'info': 'You will receive a confirmation email within 5 minutes. Our team will respond within 4 working hours.'
        }, status=status.HTTP_201_CREATED)


class TicketStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, ticket_id):
        try:
            ticket = SupportTicket.objects.prefetch_related('replies').get(ticket_id=ticket_id)
        except SupportTicket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SupportTicketSerializer(ticket).data)


class MyTicketsView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user).order_by('-created_at')


class ReplyToTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, ticket_id):
        try:
            ticket = SupportTicket.objects.get(ticket_id=ticket_id, user=request.user)
        except SupportTicket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        message = request.data.get('message', '').strip()
        if not message:
            return Response({'error': 'Message cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        reply = TicketReply.objects.create(
            ticket=ticket,
            sender=request.user.get_full_name() or request.user.username,
            is_staff=False,
            message=message
        )
        ticket.status = 'IN_PROGRESS'
        ticket.save()
        return Response({'message': 'Reply sent', 'reply': TicketReplySerializer(reply).data},
                       status=status.HTTP_201_CREATED)


class FAQListView(generics.ListAPIView):
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = FAQ.objects.filter(is_active=True)
        section = self.request.query_params.get('section')
        if section:
            qs = qs.filter(section=section)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        # Group by section
        from collections import defaultdict
        grouped = defaultdict(list)
        for faq in qs:
            grouped[faq.section].append(FAQSerializer(faq).data)
        return Response({
            'sections': [
                {'section': k, 'section_display': dict(FAQ.SECTION_CHOICES).get(k, k), 'faqs': v}
                for k, v in grouped.items()
            ]
        })
