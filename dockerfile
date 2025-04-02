# Gunakan base image Python
FROM python:3.10-slim

# Install dependencies yang diperlukan
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -N "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/linux64/chromedriver-linux64.zip" -P /tmp/ \
    && unzip /tmp/chromedriver-linux64.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver-linux64.zip /tmp/chromedriver-linux64

# Set working directory
WORKDIR /app

# Copy semua file ke dalam container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan bot absen saat container start
CMD ["python", "Absen.py"]
