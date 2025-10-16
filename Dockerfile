# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем необходимые зависимости
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копируем весь проект внутрь контейнера
COPY . /app
WORKDIR /app

# Точка входа по умолчанию
CMD ["pytest", "--alluredir=allure-results"]
