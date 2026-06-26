from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from prometheus_client import generate_latest
from starlette.responses import Response
import time
import random
import psutil

from metrics import *

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"

)


templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def monitor_requests(request: Request, call_next):

    start_time = time.time()

    REQUEST_COUNT.inc()

    response = await call_next(request)

    process_time = time.time() - start_time

    RESPONSE_TIME.observe(process_time)

    if response.status_code >= 500:
        ERROR_COUNT.inc()

    return response


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    update_system_metrics()

    alerts = []

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    if cpu > 80:
        alerts.append("HIGH CPU DETECTED")

    if memory > 80:
        alerts.append("HIGH MEMORY DETECTED")

    security_events = [
        "Failed SSH Login",
        "Port Scan Detected",
        "Multiple Login Attempts",
        "User Authentication Success"
    ]

    return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={
        "cpu": cpu,
        "memory": memory,
        "events": random.sample(security_events, 3),
        "alerts": alerts
    }
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics():

    update_system_metrics()

    return Response(
        generate_latest(),
        media_type="text/plain"
    )