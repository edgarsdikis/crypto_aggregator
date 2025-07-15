# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

ARG DEV=false

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    if [ "$DEV" = "true" ] ; then pip install --no-cache-dir -r requirements-dev.txt ; fi

# Copy project
COPY . /app/

# Copy startup script and make it executable
COPY scripts/start.sh /app/scripts/start.sh
RUN chmod +x /app/scripts/start.sh

# Create a non-root user
RUN adduser --disabled-password --gecos '' app_user
RUN chown -R app_user:app_user /app
USER app_user

# Use startup script
CMD ["/app/scripts/start.sh"]
