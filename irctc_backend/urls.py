from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class APIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Welcome to IRCTC Clone API",
            "version": "2.0",
            "endpoints": {
                "auth": {
                    "register": "/api/auth/register/",
                    "login": "/api/auth/login/",
                    "logout": "/api/auth/logout/",
                    "token_refresh": "/api/auth/token/refresh/",
                    "profile": "/api/auth/profile/",
                    "change_password": "/api/auth/change-password/",
                },
                "trains": {
                    "search_stations": "/api/trains/stations/?q=Mumbai",
                    "search_trains": "/api/trains/search/?from=CSTM&to=NDLS&date=2026-05-01",
                    "train_detail": "/api/trains/12301/",
                    "seat_availability": "/api/trains/12301/availability/?date=2026-05-01",
                },
                "bookings": {
                    "book_ticket": "POST /api/bookings/book/",
                    "pnr_status": "/api/bookings/pnr/<pnr>/",
                    "my_bookings": "/api/bookings/my-bookings/",
                    "booking_detail": "/api/bookings/<id>/",
                    "cancel_booking": "POST /api/bookings/<id>/cancel/",
                },
                "services": {
                    "live_train_status": "/api/services/live/12301/?date=2026-05-01",
                    "platform_info": "/api/services/platform/?station=CSTM",
                    "train_alerts": "/api/services/alerts/",
                    "catering_menu": "/api/services/catering/menu/?station=CSTM",
                    "catering_orders": "/api/services/catering/orders/",
                    "season_pass": "/api/services/season-pass/",
                    "tour_packages": "/api/services/tours/",
                    "tour_detail": "/api/services/tours/<id>/",
                },
                "support": {
                    "submit_ticket": "POST /api/support/ticket/",
                    "ticket_status": "/api/support/ticket/<ticket_id>/",
                    "my_tickets": "/api/support/my-tickets/",
                    "reply_to_ticket": "POST /api/support/ticket/<ticket_id>/reply/",
                    "faq": "/api/support/faq/",
                },
                "admin": "/admin/",
            }
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', APIRootView.as_view(), name='api_root'),
    path('api/auth/', include('users.urls')),
    path('api/trains/', include('trains.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/services/', include('services.urls')),
    path('api/support/', include('support.urls')),
]
