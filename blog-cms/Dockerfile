FROM python:3.11-slim

# Install git (required for GitPython)
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ /app/

# Create directory for repository mount
RUN mkdir -p /repo

# Create user with matching UID/GID (1001:1002)
RUN groupadd -g 1002 appuser && \
    useradd -u 1001 -g 1002 -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app /repo

# Switch to appuser
USER appuser

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=main.py
ENV PYTHONUNBUFFERED=1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "main:app"]
