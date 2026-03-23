from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.list_conversations, name='chat-conversations'),
    path('<int:user_id>/messages/', views.chat_messages, name='chat-messages'),
]
