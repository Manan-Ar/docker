from extensions import db


class Student(db.Model):
    """Represents a student enrolled in the system."""

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    # One student can have many grade records
    grades = db.relationship("Grade", backref="student", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "roll_number": self.roll_number,
            "course": self.course,
        }


class Grade(db.Model):
    """Represents a subject grade for a student."""

    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    grade_letter = db.Column(db.String(5), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "marks": self.marks,
            "grade_letter": self.grade_letter,
            "student_id": self.student_id,
        }
