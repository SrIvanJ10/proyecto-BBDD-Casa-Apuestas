import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.models import Usuario

print("🔍 Verificando usuarios en la base de datos...")
usuarios = Usuario.objects.all()
print(f"\n📊 Total de usuarios: {usuarios.count()}\n")

if usuarios.count() > 0:
    print("👥 Lista de usuarios:")
    for u in usuarios:
        print(f"  - Username: {u.username}")
        print(f"    Email: {u.email}")
        print(f"    Activo: {u.is_active}")
        print(f"    Es superusuario: {u.is_superuser}")
        print()
else:
    print("❌ No hay usuarios en la base de datos")
    print("\n📝 Creando usuarios de prueba...")
    
    # Crear usuario admin
    admin = Usuario.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        is_active=True,
        is_superuser=True,
        is_staff=True
    )
    print(f"✅ Usuario creado: {admin.username} / Contraseña: admin123")
    
    # Crear usuario de prueba normal
    user = Usuario.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='test123',
        first_name='Test',
        last_name='User',
        is_active=True
    )
    print(f"✅ Usuario creado: {user.username} / Contraseña: test123")
    
    print("\n🎉 Usuarios de prueba creados exitosamente!")
    print("\nCredenciales para login:")
    print("  Admin: admin / admin123")
    print("  User:  testuser / test123")
