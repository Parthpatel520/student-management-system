from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time


from app.models import *
from app.routers import auth, student, course, enrollment, grade

app = FastAPI()

# PROMETHEUS METRICS
REQUEST_COUNT = Counter("http_requests_total", "Total API Requests")
REQUEST_TIME = Histogram("http_request_duration_seconds", "Request processing time")

# Home Page
@app.get("/")
def welcome():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Student Management System</title>
        </head>
        <body>
            <h1>Welcome to Student Management System</h1>
            <p>This API helps manage students, courses, enrollments, and grades.</p>

            <a href="/docs">OpenAPI Docs</a><br>
            <a href="/redoc">ReDoc</a><br>
            <a href="/students/All">Students</a><br>
            <a href="/courses/All">Courses</a><br>
            <a href="/enrollments/All">Enrollments</a><br>
            <a href="/grades/All">Grades</a><br>
        </body>
        </html>
        """
    )

# Routers
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(grade.router)

# Middleware to track request count and response time
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    REQUEST_COUNT.inc()
    REQUEST_TIME.observe(time.time() - start_time)
    return response

# Metrics endpoint for Prometheus
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)