from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='user-profile-update'),
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4e74b6e (v1.0)
    path('update-username/', views.update_username, name='update-username'),
    path('update-password/', views.update_password, name='update-password'),
    path('leaderboard/', views.leaderboard, name='user-leaderboard'),
    path('activity/', views.user_activity, name='user-activity'),
    path('upgrade-subscription/', views.upgrade_subscription, name='upgrade-subscription'),
<<<<<<< HEAD
=======
    path('leaderboard/', views.leaderboard, name='user-leaderboard'),
    path('activity/', views.user_activity, name='user-activity'),
>>>>>>> d381094 (v0.14)
=======
>>>>>>> db693ad (v0.9)
]
