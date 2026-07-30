from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest
import os

app = FastAPI()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")

APP_NAME = os.getenv("APP_NAME", "Cloud Native DevOps Platform")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

@app.get("/")
def home():
    REQUEST_COUNT.inc()
    return {
        "application": APP_NAME,
        "environment": ENVIRONMENT,
        "status": "Running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/version")
def version():
    return {"version": "1.0.0"}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest().decode("utf-8"))