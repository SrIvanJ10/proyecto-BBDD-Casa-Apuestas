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

# Actualizar pip e instalar wheel
RUN pip install --no-cache-dir --upgrade pip wheel

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Mostrar contenido del directorio para depuración
RUN echo "Contenido del directorio /app:" && ls -la /app

# Exponer puerto
EXPOSE 8000

# Ejecutar migraciones y arrancar el servidor
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]