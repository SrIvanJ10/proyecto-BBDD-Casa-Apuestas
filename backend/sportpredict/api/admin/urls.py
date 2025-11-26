from django.urls import path
from . import views

urlpatterns = [
    # Users
    path('users/', views.admin_users_list, name='admin-users-list'),
    path('users/<int:user_id>/', views.admin_user_delete, name='admin-user-delete'),
    
    # Sports
    path('sports/', views.admin_sports_list, name='admin-sports-list'),
    path('sports/create/', views.admin_sport_create, name='admin-sport-create'),
    path('sports/<int:sport_id>/', views.admin_sport_delete, name='admin-sport-delete'),
    
    # Teams
    path('teams/', views.admin_teams_list, name='admin-teams-list'),
    path('teams/create/', views.admin_team_create, name='admin-team-create'),
    path('teams/<int:team_id>/', views.admin_team_delete, name='admin-team-delete'),
    
    # Matches
    path('matches/', views.admin_matches_list, name='admin-matches-list'),
    path('matches/create/', views.admin_match_create, name='admin-match-create'),
    path('matches/<int:match_id>/', views.admin_match_update, name='admin-match-update'),
    path('matches/<int:match_id>/delete/', views.admin_match_delete, name='admin-match-delete'),
    
    # Predictions
    path('predictions/', views.admin_predictions_list, name='admin-predictions-list'),
    path('predictions/<int:prediction_id>/', views.admin_prediction_delete, name='admin-prediction-delete'),
]
