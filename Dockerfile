# Stage 1: Tailwind CSS
FROM node:24 AS frontend-builder

# Set the working directory
WORKDIR /app

# Copy package files for better caching
COPY package*.json ./

# Install Node.js dependencies (Tailwind CSS, PostCSS, Autoprefixer)
RUN npm install

# Copy application files (your HTML templates, etc.)
COPY . .

RUN npm run build


# Stage 2: Python dependencies (builder)
FROM python:3.13-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install Python dependencies to a temporary location
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 3: Production
FROM python:3.13-slim AS production

# Environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=depo_crud.settings.production

# Install runtime dependencies (MySQL client library)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a user
RUN useradd -m -r depouser
WORKDIR /app

# Copy installed Python dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=depouser:depouser . .

# Copy static files from Tailwind stage
COPY --from=frontend-builder --chown=depouser:depouser /app/static/ /app/static/

# Prepare directories and permissions
RUN mkdir -p /app/staticfiles && chown -R depouser:depouser /app/staticfiles

# Handle entrypoint
COPY --chown=depouser:depouser entrypoint.prod.sh /app/entrypoint.prod.sh
RUN sed -i 's/\r$//' /app/entrypoint.prod.sh && chmod +x /app/entrypoint.prod.sh

USER depouser
EXPOSE 8000

# Healthcheck: checks /health/ endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

ENTRYPOINT ["/app/entrypoint.prod.sh"]
