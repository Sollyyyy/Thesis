FROM docker.io/library/python:3.11-slim

WORKDIR /app

# Install system deps for Playwright chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libgbm1 libnss3 libxcomposite1 libxdamage1 libxrandr2 \
    libpango-1.0-0 libcairo2 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
