FROM python:3.9

WORKDIR /app

# Copiar y instalar las dependencias definidas en requirements.txt
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el contenido del bot (la nueva estructura de directorios)
COPY . /app

# Ejecutar el bot 
CMD ["python", "main.py"]
