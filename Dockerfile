# Use official Python
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (needed for lxml + python-docx)
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file first (for caching)
COPY requirements.txt .

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy whole project
COPY . .

# Create Fly.io writable directory
RUN mkdir -p /data/uploads

# Environment vars
ENV FLASK_ENV=production
ENV PORT=8080

# Expose port
EXPOSE 8080

# Start server with Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
