-- Initialise the gradesdb schema with sample seed data.
-- This script runs automatically when the PostgreSQL container starts for the first time.

-- Create tables first (init.sql runs before Flask/SQLAlchemy connects).
-- IF NOT EXISTS keeps this compatible with SQLAlchemy's own create_all().

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    course VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    marks FLOAT NOT NULL,
    grade_letter VARCHAR(5) NOT NULL,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE
);

-- Seed initial student records
INSERT INTO students (name, roll_number, course)
VALUES
    ('Manan Arora',    'CS2024001', 'Containerisation and DevOps'),
    ('Priya Sharma',   'CS2024002', 'Containerisation and DevOps'),
    ('Rahul Mehta',    'CS2024003', 'Cloud Computing')
ON CONFLICT (roll_number) DO NOTHING;

-- Seed a few grade records
INSERT INTO grades (subject, marks, grade_letter, student_id)
VALUES
    ('Docker Fundamentals',      88, 'A',  1),
    ('Kubernetes Orchestration', 76, 'B',  1),
    ('CI/CD Pipelines',          92, 'A+', 1),
    ('Docker Fundamentals',      65, 'C',  2),
    ('Kubernetes Orchestration', 55, 'D',  2),
    ('Networking in the Cloud',  80, 'A',  3);
