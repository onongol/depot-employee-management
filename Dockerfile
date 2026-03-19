# Stage 1: Tailwind CSS build stage
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


# Stage 2: Python dependencies build stage
FROM python:3.14-slim AS builder

# Set the working directory
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY requirements.txt .

# Создаём venv и устанавливаем зависимости
RUN python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt


# Stage 3: Production stage
FROM python:3.14-slim AS production

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m -r depouser && \
    mkdir /app && \
    chown -R depouser /app

WORKDIR /app

# Копируем только venv — не зависит от версии Python
COPY --from=builder --chown=depouser:depouser /app/.venv /app/.venv

COPY --chown=depouser:depouser . .

# Copy the built CSS from the Tailwind stage
COPY --from=frontend-builder --chown=depouser:depouser /app/static/ /app/static/

# Switch to root user
USER root

# Create static files directory
RUN mkdir -p /app/staticfiles && chown -R depouser:depouser /app/staticfiles

# Copy entrypoint script
COPY entrypoint.prod.sh /app/entrypoint.prod.sh
RUN sed -i 's/\r$//' /app/entrypoint.prod.sh && chmod +x /app/entrypoint.prod.sh

# Switch to non-root user
USER depouser

# Expose the application port
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.prod.sh"]
