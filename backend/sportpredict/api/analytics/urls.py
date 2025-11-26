from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_metrics, name='analytics-dashboard'),
    path('stats/', views.advanced_stats, name='analytics-stats'),
    path('historical/', views.historical_dashboard, name='analytics-historical'),
    path('update/', views.update_dashboard, name='analytics-update'),
]
