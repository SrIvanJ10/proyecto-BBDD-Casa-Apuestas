FROM python:3.11-alpine

WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Mostrar contenido del directorio para depuración
RUN echo "Contenido del directorio /app:" && ls -la /app

# Exponer puerto
EXPOSE 8000

# Comando para depuración antes de ejecutar manage.py
CMD ["sh", "-c", "echo 'Listando directorio antes de ejecutar:' && ls -la && python manage.py runserver 0.0.0.0:8000"]