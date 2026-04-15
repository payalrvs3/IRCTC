from django.urls import path
from .views import (LiveTrainStatusView, PlatformInfoView,
                    TrainAlertListCreateView, TrainAlertDeleteView,
                    CateringMenuView, CateringOrderView,
                    SeasonPassListCreateView, TourPackageListView, TourPackageDetailView)

urlpatterns = [
    path('live/<str:train_number>/', LiveTrainStatusView.as_view(), name='live_status'),
    path('platform/', PlatformInfoView.as_view(), name='platform_info'),
    path('alerts/', TrainAlertListCreateView.as_view(), name='alerts'),
    path('alerts/<int:pk>/', TrainAlertDeleteView.as_view(), name='alert_delete'),
    path('catering/menu/', CateringMenuView.as_view(), name='catering_menu'),
    path('catering/orders/', CateringOrderView.as_view(), name='catering_orders'),
    path('season-pass/', SeasonPassListCreateView.as_view(), name='season_pass'),
    path('tours/', TourPackageListView.as_view(), name='tour_packages'),
    path('tours/<int:pk>/', TourPackageDetailView.as_view(), name='tour_detail'),
]
