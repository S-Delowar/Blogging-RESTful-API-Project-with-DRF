# Base image
FROM python:3.11-slim

# Setting environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setting work directory
WORKDIR /app

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installing Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copying project files
COPY . .

# Collecting static files
RUN python manage.py collectstatic --noinput

# Exposing the port
EXPOSE 8000

# Running the application using Gunicorn
CMD ["gunicorn", "blogapi.wsgi:application", "--bind", "0.0.0.0:8000"]
