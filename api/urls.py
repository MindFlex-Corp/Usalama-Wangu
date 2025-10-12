from django.urls import path
from . import views

urlpatterns = [
    path('alert/', views.AlertListCreateView.as_view()),
    path('sms/<int:alert_id>', views.AlertSMSHistoryView.as_view()),
    path('zones/', views.ZoneList.as_view()),
    path('zones/<int:pk>/', views.ZoneDetail.as_view()),
]
