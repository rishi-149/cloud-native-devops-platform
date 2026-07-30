FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are sent directly to stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user
RUN useradd -m appuser

# Switch to the non-root user
USER appuser

EXPOSE 8000

# Health check for the application
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]