# Используем базовый образ Python 3.9
FROM python:3.8-slim-buster

WORKDIR /app

# Копируем файлы приложения
COPY . /app

# Устанавливаем зависимости из файла requirements/base.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements/base.txt

# Запускаем приложение
CMD ["python3",  "start.py"]