# app/main.py
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .health import get_liveness, get_readiness
from .reliability import flaky_with_retries

app = FastAPI(title="Reliability Reference Microservice")

# Metrics: /metrics
Instrumentator().instrument(app).expose(app)


@app.get("/health/live")
def liveness():
    return get_liveness()


@app.get("/health/ready")
def readiness():
    return get_readiness()


@app.get("/demo")
def demo_endpoint():
    return {
        "result": flaky_with_retries(),
        "circuit_state": breaker.state.value,
    }

