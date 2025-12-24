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

# Run the Tailwind CSS build command
#RUN npm run build:css

# Build JavaScript assets
#RUN npm run build:js

RUN npm run build


# Stage 2: Python dependencies build stage
FROM python:3.13 AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Stage 3: Production stage
FROM python:3.13 AS production

# Create a non-root user "depouser"
RUN useradd -m -r depouser && \
    mkdir /app && \
    chown -R depouser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=depouser:depouser . .

# Copy the built CSS from the Tailwind stage
# COPY --from=frontend-builder --chown=depouser:depouser /app/static/dist/ /app/static/dist/
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
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "depo_crud.wsgi:application"]
