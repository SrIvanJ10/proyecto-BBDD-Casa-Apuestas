from django.urls import path
from . import views

urlpatterns = [
    path('', views.matches_list, name='matches-list'),
    path('<int:match_id>/', views.match_detail, name='match-detail'),
    path('upcoming/', views.upcoming_matches, name='matches-upcoming'),
    path('live/', views.live_matches, name='matches-live'),
    path('finished/', views.finished_matches, name='matches-finished'),
]
