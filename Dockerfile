FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash raiderbot
USER raiderbot

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "from server import sf_client; print('healthy' if sf_client.health_check()['status'] == 'healthy' else exit(1))"

# Start application
CMD ["python", "server.py"]
