from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database import Base, engine
from app.models import *
from app.routers import auth, student, course, enrollment, grade

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(grade.router)



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
            <style>
                :root {
                    --bg: #f4f8ff;
                    --card: #ffffff;
                    --text: #1f2937;
                    --sub: #4b5563;
                    --primary: #0f766e;
                    --border: #dbe3ef;
                }
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    min-height: 100vh;
                    display: grid;
                    place-items: center;
                    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                    background: radial-gradient(circle at 20% 20%, #d6e8ff, var(--bg));
                    color: var(--text);
                    padding: 24px;
                }
                .card {
                    width: min(760px, 100%);
                    background: var(--card);
                    border: 1px solid var(--border);
                    border-radius: 18px;
                    padding: 32px;
                    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
                }
                h1 {
                    margin-top: 0;
                    margin-bottom: 10px;
                    font-size: clamp(1.7rem, 2.5vw, 2.3rem);
                }
                p {
                    margin: 0 0 18px;
                    color: var(--sub);
                    line-height: 1.5;
                }
                .links {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-top: 10px;
                }
                a {
                    text-decoration: none;
                    padding: 10px 14px;
                    border-radius: 10px;
                    border: 1px solid var(--border);
                    color: var(--text);
                    background: #f9fbff;
                    transition: 0.2s ease;
                }
                a:hover {
                    border-color: var(--primary);
                    color: var(--primary);
                    transform: translateY(-1px);
                }
            </style>
        </head>
        <body>
            <main class="card">
                <h1>Welcome to Student Management System</h1>
                <p>
                    This API helps manage students, courses, enrollments, and grades.
                    Use the links below to explore and test available endpoints.
                </p>
                <div class="links">
                    <a href="/docs">OpenAPI Docs</a>
                    <a href="/redoc">ReDoc</a>
                    <a href="/students/All">Students</a>
                    <a href="/courses/All">Courses</a>
                    <a href="/enrollments/All">Enrollments</a>
                    <a href="/grades/All">Grades</a>
                </div>
            </main>
        </body>
        </html>
        """
    )
