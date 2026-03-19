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

# Устанавливаем ВСЕ зависимости для сборки (включая python3-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Устанавливаем зависимости в локальную папку, чтобы легко скопировать
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 3: Production stage
FROM python:3.14-slim AS production

# Важно: устанавливаем runtime-библиотеку mysql
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя
RUN useradd -m -r depouser
WORKDIR /app

# Копируем установленные библиотеки из builder
# Это надежнее, чем копировать .venv с жесткими путями
COPY --from=builder /install /usr/local

# Копируем код приложения
COPY --chown=depouser:depouser . .

# Копируем статику из Tailwind этапа
COPY --from=frontend-builder --chown=depouser:depouser /app/static/ /app/static/

# Подготовка папок и прав
RUN mkdir -p /app/staticfiles && chown -R depouser:depouser /app/staticfiles

# Обработка entrypoint
COPY --chown=depouser:depouser entrypoint.prod.sh /app/entrypoint.prod.sh
RUN sed -i 's/\r$//' /app/entrypoint.prod.sh && chmod +x /app/entrypoint.prod.sh

USER depouser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.prod.sh"]
