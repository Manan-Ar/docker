from flask import Blueprint, request, jsonify
from extensions import db
from models import Student, Grade

api = Blueprint("api", __name__)


def calculate_grade_letter(marks):
    """Convert a numerical mark to a letter grade."""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------------------------
# Student Endpoints
# ---------------------------------------------------------------------------

@api.route("/students", methods=["GET"])
def get_all_students():
    """Return a list of all registered students."""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200


@api.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Return a single student by ID."""
    student = Student.query.get_or_404(student_id, description="Student not found.")
    return jsonify(student.to_dict()), 200


@api.route("/students", methods=["POST"])
def create_student():
    """Register a new student."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    required_fields = ["name", "roll_number", "course"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Check for duplicate roll number
    if Student.query.filter_by(roll_number=data["roll_number"]).first():
        return jsonify({"error": "A student with this roll number already exists."}), 409

    student = Student(
        name=data["name"].strip(),
        roll_number=data["roll_number"].strip(),
        course=data["course"].strip(),
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@api.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """Update a student's details."""
    student = Student.query.get_or_404(student_id, description="Student not found.")
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    student.name = data.get("name", student.name).strip()
    student.course = data.get("course", student.course).strip()

    db.session.commit()
    return jsonify(student.to_dict()), 200


@api.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student and all their associated grades."""
    student = Student.query.get_or_404(student_id, description="Student not found.")
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Student '{student.name}' deleted successfully."}), 200


# ---------------------------------------------------------------------------
# Grade Endpoints
# ---------------------------------------------------------------------------

@api.route("/students/<int:student_id>/grades", methods=["GET"])
def get_grades(student_id):
    """Return all grades for a specific student."""
    student = Student.query.get_or_404(student_id, description="Student not found.")
    grades = [g.to_dict() for g in student.grades]
    return jsonify({"student": student.to_dict(), "grades": grades}), 200


@api.route("/students/<int:student_id>/grades", methods=["POST"])
def add_grade(student_id):
    """Add a grade entry for a student."""
    Student.query.get_or_404(student_id, description="Student not found.")
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    required_fields = ["subject", "marks"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    marks = data["marks"]
    if not isinstance(marks, (int, float)) or not (0 <= marks <= 100):
        return jsonify({"error": "Marks must be a number between 0 and 100."}), 400

    grade = Grade(
        subject=data["subject"].strip(),
        marks=marks,
        grade_letter=calculate_grade_letter(marks),
        student_id=student_id,
    )
    db.session.add(grade)
    db.session.commit()
    return jsonify(grade.to_dict()), 201


@api.route("/students/<int:student_id>/grades/<int:grade_id>", methods=["DELETE"])
def delete_grade(student_id, grade_id):
    """Remove a specific grade entry."""
    grade = Grade.query.filter_by(id=grade_id, student_id=student_id).first_or_404(
        description="Grade record not found."
    )
    db.session.delete(grade)
    db.session.commit()
    return jsonify({"message": "Grade deleted successfully."}), 200


# ---------------------------------------------------------------------------
# Summary Endpoint
# ---------------------------------------------------------------------------

@api.route("/students/<int:student_id>/summary", methods=["GET"])
def student_summary(student_id):
    """Return a summary with average marks and overall grade for a student."""
    student = Student.query.get_or_404(student_id, description="Student not found.")

    if not student.grades:
        return jsonify({"message": "No grades recorded for this student."}), 200

    total_marks = sum(g.marks for g in student.grades)
    average = round(total_marks / len(student.grades), 2)

    return jsonify({
        "student": student.to_dict(),
        "total_subjects": len(student.grades),
        "average_marks": average,
        "overall_grade": calculate_grade_letter(average),
    }), 200
