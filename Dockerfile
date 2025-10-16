# Базовый образ с Python и Chrome
FROM python:3.12-slim

# Устанавливаем зависимости для Chrome и Xvfb
RUN apt-get update && apt-get install -y \
    wget unzip curl xvfb gnupg \
    libnss3 libgconf-2-4 libxi6 libxss1 libx11-xcb1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Устанавливаем ChromeDriver соответствующей версии Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) \
    && LATEST=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") \
    && wget -q "https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем проект
COPY . /app

# Запуск тестов через xvfb-run
ENTRYPOINT ["xvfb-run", "-a", "pytest", "--alluredir=/app/allure-results"]
