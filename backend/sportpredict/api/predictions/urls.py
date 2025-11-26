from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_predictions, name='predictions-list'),
    path('create/', views.create_prediction, name='predictions-create'),
    path('stats/', views.prediction_stats, name='predictions-stats'),
    path('match/<int:match_id>/', views.match_predictions, name='predictions-match'),
    path('<int:prediction_id>/', views.prediction_detail, name='prediction-detail'),
    path('<int:prediction_id>/update/', views.update_prediction, name='prediction-update'),
    path('<int:prediction_id>/delete/', views.delete_prediction, name='prediction-delete'),
]
