from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='user-profile-update'),
    path('leaderboard/', views.leaderboard, name='user-leaderboard'),
    path('activity/', views.user_activity, name='user-activity'),
    path('upgrade-subscription/', views.upgrade_subscription, name='upgrade-subscription'),
]
