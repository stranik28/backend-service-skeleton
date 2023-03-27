# Используем базовый образ Python 3.8
FROM python:3.8-slim-buster

# Установка зависимостей операционной системы и приложения
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файлы приложения
COPY . /app

# Устанавливаем зависимости из файла requirements/base.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements/base.txt

# Устанавливаем переменную среды PYTHONUNBUFFERED для unbuffered вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем переменную среды для порта, который будет использоваться в контейнере
ENV PORT=8000

# Запускаем приложение
CMD ["python3", "start.py"]
