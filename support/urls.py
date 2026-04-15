from django.urls import path
from .views import SubmitTicketView, TicketStatusView, MyTicketsView, ReplyToTicketView, FAQListView

urlpatterns = [
    path('ticket/', SubmitTicketView.as_view(), name='submit_ticket'),
    path('ticket/<str:ticket_id>/', TicketStatusView.as_view(), name='ticket_status'),
    path('my-tickets/', MyTicketsView.as_view(), name='my_tickets'),
    path('ticket/<str:ticket_id>/reply/', ReplyToTicketView.as_view(), name='ticket_reply'),
    path('faq/', FAQListView.as_view(), name='faq'),
]
