from django.urls import path, include
from . import views

urlpatterns = [
    # 🔧 Test endpoint - Para verificar que el backend funciona
    path('test/', views.test_api, name='test-api'),

    # 🔐 Authentication endpoints
    path('auth/', include('sportpredict.api.auth.urls')),

    # ⚽ Matches endpoints
    path('matches/', include('sportpredict.api.matches.urls')),

    # 📊 Analytics endpoints
    path('analytics/', include('sportpredict.api.analytics.urls')),
    
    # ⚙️ Admin endpoints
    path('admin/', include('sportpredict.api.admin.urls')),  # Admin panel routes
    
    # 🎯 Recommendations endpoints (para el futuro)
    path('recommendations/', include('sportpredict.api.recommendations.urls')),

    # 👤 Users endpoints
    path('users/', include('sportpredict.api.users.urls')),

    # 👥 Friends endpoints
    path('friends/', include('sportpredict.api.friends.urls')),

    # 💬 Chat endpoints
    path('chat/', include('sportpredict.api.chat.urls')),
    
    # 🏆 Predictions endpoints (para el futuro)
    path('predictions/', include('sportpredict.api.predictions.urls')),
]
