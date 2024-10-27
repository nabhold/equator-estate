# Use the slim Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for Pillow and other libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6-dev \
    libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and set permissions
RUN mkdir -p /app && \
    adduser -u 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser /app

RUN apt-get update && apt-get install -y postgresql-client

# Set the working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Install python-decouple
RUN python -m pip install --no-cache-dir python-decouple

# Copy the entire app code to the container
COPY . .

# Copy wait-for-it.sh into the container
COPY wait-for-it.sh /usr/local/bin/wait-for-it

# Ensure it is executable
RUN chmod +x /usr/local/bin/wait-for-it

# Copy .env file to the container
COPY .env .

# Change to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Start Celery worker, Celery beat, and Gunicorn server using wait-for-it to ensure the database is ready
#CMD ["sh", "-c", "wait-for-it db:5432 --timeout=30 --strict -- celery -A nabhold worker --loglevel=info & celery -A nabhold beat --loglevel=info & gunicorn nabhold.wsgi:application --bind 0.0.0.0:8000"]


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "nabhold.wsgi"]
