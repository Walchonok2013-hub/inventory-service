FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Копируем requirements и ставим пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .


