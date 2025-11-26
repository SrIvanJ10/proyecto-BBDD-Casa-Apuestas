FROM python:3.11-alpine

WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL y PyJWT
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .

# Actualizar pip y setuptools, e instalar wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalar PyJWT explícitamente primero (con sus dependencias criptográficas)
RUN pip install --no-cache-dir PyJWT==2.8.0

# Verificar que PyJWT se instaló correctamente
RUN python -c "import jwt; print('PyJWT installed successfully:', jwt.__version__)"

# Instalar el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Mostrar contenido del directorio para depuración
RUN echo "Contenido del directorio /app:" && ls -la /app

# Exponer puerto
EXPOSE 8000

# Comando para depuración antes de ejecutar manage.py
CMD ["sh", "-c", "echo 'Listando directorio antes de ejecutar:' && ls -la && python manage.py runserver 0.0.0.0:8000"]