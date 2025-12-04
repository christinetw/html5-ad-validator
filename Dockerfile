# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for lxml + python-docx)
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Fly.io will mount /data itself — do NOT create it here
# The app should create /data/uploads at runtime if needed
# (your app already does: os.makedirs(UPLOAD_FOLDER, exist_ok=True))

ENV FLASK_ENV=production
ENV PORT=8080

EXPOSE 8080

# Production server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
