# Use official Python image 
FROM python:3.11-slim

# Set working directory 
WORKDIR /app

# Copy all files 
COPY . .

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 
EXPOSE 8080

# Run the app 
CMD ["python", "app.py"]