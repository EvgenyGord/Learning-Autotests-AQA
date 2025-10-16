# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем зависимости для Chrome и Xvfb
RUN apt-get update && apt-get install -y \
    wget unzip curl xvfb gnupg \
    libnss3 libxi6 libxss1 libx11-xcb1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chrome
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux-signing-key.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chromedriver через webdriver-manager
RUN pip install --no-cache-dir selenium webdriver-manager pytest pytest-xdist pytest-html allure-pytest Faker

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# По умолчанию запускаем pytest (можно переопределить через docker run)
CMD ["pytest", "--alluredir=/app/allure-results"]
