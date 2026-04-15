from django.urls import path
from .views import BookTicketView, PNRStatusView, MyBookingsView, BookingDetailView, CancelBookingView

urlpatterns = [
    path('book/', BookTicketView.as_view(), name='book_ticket'),
    path('pnr/<str:pnr>/', PNRStatusView.as_view(), name='pnr_status'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel_booking'),
]
