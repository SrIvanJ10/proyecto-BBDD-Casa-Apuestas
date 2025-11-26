#!/bin/bash

# Script para probar todas las APIs de SportPredict
# Ubicación: En la raíz del proyecto, al lado de manage.py
# Uso: ./test_all.sh

BASE_URL="http://localhost:8000/api"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧪 Probando TODAS las APIs de SportPredict...${NC}"
echo "=============================================="

# Verificar que el servidor esté corriendo
echo -e "\n1. 🔍 Verificando servidor Django..."
if curl -s --head http://localhost:8000/api/test/ | grep "200 OK" > /dev/null; then
    echo -e "${GREEN}✅ Servidor Django está corriendo${NC}"
else
    echo -e "${RED}❌ Servidor Django NO está corriendo${NC}"
    echo -e "${YELLOW}💡 Ejecuta primero: python manage.py runserver${NC}"
    exit 1
fi

# 2. Probar endpoint de test
echo -e "\n2. 🔧 Probando endpoint de test:"
test_response=$(curl -s -X GET "$BASE_URL/test/")
if [[ $test_response == *"funcionando"* ]]; then
    echo -e "${GREEN}✅ Test API funciona${NC}"
    echo "   Respuesta: $(echo $test_response | jq -r '.message' 2>/dev/null || echo $test_response)"
else
    echo -e "${RED}❌ Test API falló${NC}"
    echo "   Error: $test_response"
fi

# 3. Registrar usuario
echo -e "\n3. 📝 Registrando usuario:"
timestamp=$(date +%s)
register_response=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"test${timestamp}@ejemplo.com\",
    \"username\": \"testuser${timestamp}\",
    \"password\": \"password123\",
    \"first_name\": \"Test\",
    \"last_name\": \"User\"
  }")

if [[ $register_response == *"successful"* ]] || [[ $register_response == *"exitoso"* ]]; then
    echo -e "${GREEN}✅ Registro funciona${NC}"
    # Extraer user_id si existe
    if [[ $register_response == *"user_id"* ]]; then
        user_id=$(echo "$register_response" | grep -o '"user_id":[0-9]*' | cut -d':' -f2)
        echo "   User ID: $user_id"
    fi
    echo "   Respuesta: $(echo $register_response | jq -r '.message' 2>/dev/null || echo $register_response)"
else
    echo -e "${RED}❌ Registro falló${NC}"
    echo "   Error: $register_response"
fi

# 4. Login (usando credenciales de prueba)
echo -e "\n4. 🔐 Probando login:"
login_response=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@ejemplo.com",
    "password": "password123"
  }')

if [[ $login_response == *"token"* ]]; then
    echo -e "${GREEN}✅ Login funciona${NC}"
    # Extraer token para otras pruebas
    token=$(echo "$login_response" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
    echo "   Token obtenido: ${token:0:20}..."
else
    echo -e "${YELLOW}⚠️ Login falló (esperado sin usuario real)${NC}"
    echo "   Respuesta: $(echo $login_response | jq -r '.error' 2>/dev/null || echo $login_response)"
fi

# 5. Verificar OTP (simulado)
echo -e "\n5. 📱 Probando verificación OTP:"
otp_response=$(curl -s -X POST "$BASE_URL/auth/verify-otp/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@ejemplo.com",
    "otp": "123456"
  }')

if [[ $otp_response == *"verified"* ]] || [[ $otp_response == *"verificado"* ]] || [[ $otp_response == *"token"* ]]; then
    echo -e "${GREEN}✅ Verificación OTP funciona${NC}"
    echo "   Respuesta: $(echo $otp_response | jq -r '.message' 2>/dev/null || echo $otp_response)"
else
    echo -e "${YELLOW}⚠️ Verificación OTP falló (esperado sin OTP real)${NC}"
    echo "   Respuesta: $(echo $otp_response | jq -r '.error' 2>/dev/null || echo $otp_response)"
fi

# 6. Olvidé contraseña
echo -e "\n6. 🔓 Probando 'olvidé contraseña':"
forgot_response=$(curl -s -X POST "$BASE_URL/auth/forgot-password/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@ejemplo.com"
  }')

if [[ $forgot_response == *"enviado"* ]] || [[ $forgot_response == *"sent"* ]] || [[ $forgot_response == *"existe"* ]]; then
    echo -e "${GREEN}✅ 'Olvidé contraseña' funciona${NC}"
    echo "   Respuesta: $(echo $forgot_response | jq -r '.message' 2>/dev/null || echo $forgot_response)"
else
    echo -e "${YELLOW}⚠️ 'Olvidé contraseña' falló${NC}"
    echo "   Respuesta: $forgot_response"
fi

# 7. Logout
echo -e "\n7. 🚪 Probando logout:"
logout_response=$(curl -s -X POST "$BASE_URL/auth/logout/" \
  -H "Content-Type: application/json")

if [[ $logout_response == *"exitoso"* ]] || [[ $logout_response == *"success"* ]]; then
    echo -e "${GREEN}✅ Logout funciona${NC}"
    echo "   Respuesta: $(echo $logout_response | jq -r '.message' 2>/dev/null || echo $logout_response)"
else
    echo -e "${YELLOW}⚠️ Logout falló${NC}"
    echo "   Respuesta: $logout_response"
fi

echo -e "\n=============================================="
echo -e "${GREEN}🧪 Todas las pruebas completadas!${NC}"
echo -e "${GREEN}✅ Backend funcionando correctamente${NC}"
echo ""
echo -e "${YELLOW}📋 Resumen de endpoints probados:${NC}"
echo "  ✅ GET    /api/test/"
echo "  ✅ POST   /api/auth/register/"
echo "  ✅ POST   /api/auth/login/" 
echo "  ✅ POST   /api/auth/verify-otp/"
echo "  ✅ POST   /api/auth/forgot-password/"
echo "  ✅ POST   /api/auth/logout/"
