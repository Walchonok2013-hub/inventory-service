FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для psycopg2 и сборки пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Команда по умолчанию (переопределяется в docker-compose для разных сервисов)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]