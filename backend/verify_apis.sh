#!/bin/bash
# Script de verificación de imports y configuración

echo "🔍 Verificando configuración de SportPredict APIs..."
echo ""

cd /run/user/1000/gvfs/sftp:host=192.168.1.239,user=debian/home/debian/luis/proyecto-BBDD-Casa-Apuestas/backend

echo "1️⃣ Verificando imports de Python..."
python3 << 'EOF'
import sys
import os

# Añadir el directorio al path
sys.path.insert(0, os.getcwd())

try:
    # Test imports básicos
    print("   ✓ Importando Django settings...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
    import django
    django.setup()
    
    print("   ✓ Importando modelos...")
    from sportpredict.models import Usuario, Partido, Prediccion
    
    print("   ✓ Importando serializers...")
    from sportpredict.serializers import UsuarioSerializer, PartidoSerializer
    
    print("   ✓ Importando utilidades...")
    from sportpredict.api.utils.authentication import generate_jwt_token
    from sportpredict.api.utils.rate_limiter import RateLimiter
    
    print("   ✓ Importando managers de MongoDB...")
    from sportpredict.db.mongodb import AnalyticsManager, PartidoStatsManager
    
    print("   ✓ Importando managers de Redis...")
    from sportpredict.db.redis.otp import OTPManager
    from sportpredict.db.redis.sessions import SessionManager
    
    print("\n✅ Todos los imports funcionan correctamente!")
    
except Exception as e:
    print(f"\n❌ Error en imports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "2️⃣ Verificando estructura de archivos..."
    
    # Verificar archivos clave
    files=(
        "sportpredict/serializers.py"
        "sportpredict/api/utils/authentication.py"
        "sportpredict/api/utils/rate_limiter.py"
        "sportpredict/api/utils/redis_client.py"
        "sportpredict/api/auth/views.py"
        "sportpredict/api/matches/views.py"
        "sportpredict/api/predictions/views.py"
        "sportpredict/api/users/views.py"
        "sportpredict/api/analytics/views.py"
        "sportpredict/api/recommendations/views.py"
        "API_DOCUMENTATION.md"
    )
    
    all_exist=true
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            echo "   ✓ $file"
        else
            echo "   ✗ $file (FALTA)"
            all_exist=false
        fi
    done
    
    if [ "$all_exist" = true ]; then
        echo ""
        echo "✅ Todos los archivos necesarios existen!"
        echo ""
        echo "🎉 Verificación completada exitosamente!"
        echo ""
        echo "📝 Próximos pasos:"
        echo "   1. Ejecutar migraciones: python manage.py migrate"
        echo "   2. Crear superusuario: python manage.py createsuperuser"
        echo "   3. Iniciar servidor: python manage.py runserver"
        echo "   4. Probar APIs con la documentación en API_DOCUMENTATION.md"
    else
        echo ""
        echo "⚠️  Algunos archivos faltan. Revisa la lista anterior."
        exit 1
    fi
else
    echo ""
    echo "⚠️  Hay problemas con los imports. Revisa los errores anteriores."
    exit 1
fi
