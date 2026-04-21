# Student Grade Management System

A containerized REST API for managing student records and grades, built with Flask and PostgreSQL. The entire application stack runs inside Docker containers orchestrated by Docker Compose, demonstrating core containerization and DevOps principles including multi-container networking, environment-based configuration, volume persistence, and health-check-driven service startup ordering.

---

## Features

- Full CRUD operations for student records (create, read, update, delete)
- Grade entry per student with automatic letter-grade calculation
- Per-student summary endpoint showing average marks and overall grade
- Multi-container setup with Flask API and PostgreSQL database
- Health-check dependency so the API only starts after the database is ready
- Named Docker volume for persistent data storage across container restarts
- Environment-variable-driven configuration with `.env` file support
- Seed data loaded automatically on first database initialization
- Health check endpoint (`/health`) for monitoring

---

## Tech Stack

| Layer      | Technology                   |
|------------|------------------------------|
| Language   | Python 3.12                  |
| Framework  | Flask 3.0                    |
| Database   | PostgreSQL 16                |
| ORM        | Flask-SQLAlchemy             |
| Server     | Gunicorn                     |
| Container  | Docker, Docker Compose v3.9  |

---

## Project Structure

```
Container Assignment 1/
├── app.py                  # Application factory and entry point
├── config.py               # Environment-based configuration
├── extensions.py           # Shared SQLAlchemy instance
├── models.py               # Database models (Student, Grade)
├── routes.py               # API route definitions
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image for the Flask app
├── docker-compose.yml      # Multi-container orchestration
├── .env                    # Environment variables
├── .dockerignore           # Files excluded from Docker build context
└── db/
    └── init.sql            # Database seed script
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- No Python installation required on the host machine

---

## Installation

**1. Clone the repository**

```bash
git clone <repo-link>
cd "Container Assignment 1"
```

**2. Review the environment file**

Open `.env` and adjust credentials if needed (defaults work out of the box):

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=gradesdb
```

**3. Build and start all containers**

```bash
docker-compose up --build
```

Docker Compose will:
- Build the Flask application image
- Pull the official PostgreSQL 16 image
- Start the database, wait for it to be healthy, then start the API

The API will be accessible at `http://localhost:5000`.

---

## Usage

All endpoints are prefixed with `/api`. Use any HTTP client such as `curl`, Postman, or a browser.

### Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{"status": "ok", "environment": "development"}
```

---

### Students

#### List all students
```bash
curl http://localhost:5000/api/students
```

#### Get a single student
```bash
curl http://localhost:5000/api/students/1
```

#### Create a student
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Manan Arora", "roll_number": "CS2024001", "course": "Containerisation and DevOps"}'
```

Response (`201 Created`):
```json
{
  "id": 1,
  "name": "Manan Arora",
  "roll_number": "CS2024001",
  "course": "Containerisation and DevOps"
}
```

#### Update a student
```bash
curl -X PUT http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"course": "Cloud Computing"}'
```

#### Delete a student
```bash
curl -X DELETE http://localhost:5000/api/students/1
```

---

### Grades

#### Add a grade for a student
```bash
curl -X POST http://localhost:5000/api/students/1/grades \
  -H "Content-Type: application/json" \
  -d '{"subject": "Docker Fundamentals", "marks": 88}'
```

Response (`201 Created`):
```json
{
  "id": 1,
  "subject": "Docker Fundamentals",
  "marks": 88.0,
  "grade_letter": "A",
  "student_id": 1
}
```

#### Get all grades for a student
```bash
curl http://localhost:5000/api/students/1/grades
```

#### Get student summary (average and overall grade)
```bash
curl http://localhost:5000/api/students/1/summary
```

Response:
```json
{
  "student": {"id": 1, "name": "Manan Arora", "roll_number": "CS2024001", "course": "Containerisation and DevOps"},
  "total_subjects": 3,
  "average_marks": 85.33,
  "overall_grade": "A"
}
```

---

## Grading Scale

| Marks     | Grade |
|-----------|-------|
| 90 – 100  | A+    |
| 80 – 89   | A     |
| 70 – 79   | B     |
| 60 – 69   | C     |
| 50 – 59   | D     |
| Below 50  | F     |

---

## Stopping the Application

```bash
docker-compose down
```

To also remove the persistent volume (clears all database data):

```bash
docker-compose down -v
```

---

## Notes

- The seed data in `db/init.sql` only runs once, on the very first container startup when the volume is empty. If data already exists, the script is skipped.
- The API waits for PostgreSQL to pass its health check before accepting requests, preventing connection errors during startup.
- All configuration is externalized through environment variables, following the twelve-factor app methodology.
- The Dockerfile uses `python:3.12-slim` to minimize the image size.

---

## Author

**Name:** Manan Arora  
**Course:** Containerisation and DevOps
