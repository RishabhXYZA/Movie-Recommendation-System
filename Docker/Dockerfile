# Use a slim version of Python to save RAM
FROM python:3.10-slim

# Set environment variables to optimize Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies without cache to save disk space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (app.py, .pkl files, etc.)
COPY . .

# Railway provides a dynamic PORT, so we use the $PORT variable
# This is the key to fixing the "Service Not Available" error on mobile
CMD gunicorn app:app --bind 0.0.0.0:$PORT
