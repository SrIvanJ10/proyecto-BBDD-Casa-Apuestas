from django.urls import path, include
from . import views

urlpatterns = [
    # 🔧 Test endpoint - Para verificar que el backend funciona
    path('test/', views.test_api, name='test-api'),
    
    # 🔐 Authentication endpoints
    path('auth/', include('sportpredict.api.auth.urls')),
    
    # ⚽ Matches endpoints (por si los añades después)
    path('matches/', include('sportpredict.api.matches.urls')),
    
    # 📊 Analytics endpoints (para el futuro)
    path('analytics/', include('sportpredict.api.analytics.urls')),
    
<<<<<<< HEAD
<<<<<<< HEAD
    # ⚙️ Admin endpoints
    path('admin/', include('sportpredict.api.admin.urls')),  # Admin panel routes
    
=======
>>>>>>> d381094 (v0.14)
=======
    # ⚙️ Admin endpoints
    path('admin/', include('sportpredict.api.admin.urls')),  # Admin panel routes
    
>>>>>>> 4e74b6e (v1.0)
    # 🎯 Recommendations endpoints (para el futuro)
    path('recommendations/', include('sportpredict.api.recommendations.urls')),
    
    # 👤 Users endpoints (para el futuro)
    path('users/', include('sportpredict.api.users.urls')),
    
    # 👥 Friends endpoints
    path('friends/', include('sportpredict.api.friends.urls')),
    
    # 🏆 Predictions endpoints (para el futuro)
    path('predictions/', include('sportpredict.api.predictions.urls')),
]
