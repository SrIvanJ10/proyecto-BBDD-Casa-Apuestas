from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.recommended_matches, name='recommendations-matches'),
    path('users/', views.similar_users, name='recommendations-users'),
    path('trending/', views.trending_matches, name='recommendations-trending'),
    path('debug-neo4j/', views.debug_neo4j, name='debug-neo4j'),
]
