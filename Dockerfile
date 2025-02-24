# Usa una imagen ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación al contenedor
COPY . .

# Especifica el comando para ejecutar el bot
CMD ["python", "main.py"]
