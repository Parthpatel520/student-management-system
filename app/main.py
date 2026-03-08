from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.responses import Response

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

import time
import logging
import sentry_sdk

from app.models import *
from app.routers import auth, student, course, enrollment, grade


# ---------------- SENTRY SETUP ----------------
sentry_sdk.init(
    dsn="https://25d8908435c57a0f8d4d59b3ba363e58@o4510991203958784.ingest.us.sentry.io/4510991210971136",
    send_default_pii=True,
)


# ---------------- LOGGING SETUP (ELK) ----------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------- FASTAPI APP ----------------
app = FastAPI()


# ---------------- PROMETHEUS METRICS ----------------
REQUEST_COUNT = Counter("http_requests_total", "Total API Requests")
REQUEST_TIME = Histogram("http_request_duration_seconds", "Request processing time")


# ---------------- HOME PAGE ----------------
@app.get("/")
def welcome():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Management System</title>
        </head>
        <body>

            <h1>Welcome to Student Management System</h1>

            <p>This API helps manage students, courses, enrollments, and grades.</p>

            <h3>API Links</h3>

            <a href="/docs">Swagger Docs</a><br>
            <a href="/redoc">ReDoc</a><br>
            <a href="/students/All">Students</a><br>
            <a href="/courses/All">Courses</a><br>
            <a href="/enrollments/All">Enrollments</a><br>
            <a href="/grades/All">Grades</a><br>

        </body>
        </html>
        """
    )


# ---------------- INCLUDE ROUTERS ----------------
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(grade.router)


# ---------------- REQUEST MONITORING MIDDLEWARE ----------------
@app.middleware("http")
async def monitor_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    # Prometheus Metrics
    REQUEST_COUNT.inc()
    REQUEST_TIME.observe(process_time)

    # Logging for ELK
    logger.info(f"{request.method} {request.url.path} completed in {process_time:.4f} sec")

    return response


# ---------------- PROMETHEUS METRICS ENDPOINT ----------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---------------- SENTRY TEST ERROR ----------------
@app.get("/sentry-error")
def error():
    division_by_zero = 1 / 0
    return {"result": division_by_zero}