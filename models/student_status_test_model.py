# models/student_status_test_model.py
from sqlalchemy import CheckConstraint, func
from datetime import datetime
from database import db

class StudentStatusTest(db.Model):
    __tablename__ = 'student_status_tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    grade_level = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    questions = db.relationship(
        'TestQuestion',
        back_populates='test',
        cascade='all, delete-orphan',
        order_by='TestQuestion.position'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "gradeLevel": self.grade_level,
            "subject": self.subject,
            "createdAt": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            "questions": [q.to_dict() for q in self.questions]
        }


class TestQuestion(db.Model):
    __tablename__ = 'test_questions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('student_status_tests.id', ondelete='CASCADE'), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)  # 0..N
    statement = db.Column(db.Text, nullable=False)

    test = db.relationship('StudentStatusTest', back_populates='questions')
    options = db.relationship(
        'TestOption',
        back_populates='question',
        cascade='all, delete-orphan',
        order_by='TestOption.position'
    )

    __table_args__ = (
        CheckConstraint('position >= 0', name='ck_question_position_nonnegative'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "statement": self.statement,
            "options": [o.to_dict() for o in self.options],
            "correctIndex": next((o.position for o in self.options if o.is_correct), None)
        }


class TestOption(db.Model):
    __tablename__ = 'test_options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('test_questions.id', ondelete='CASCADE'), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)  # 0..3
    text = db.Column(db.String(300), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    question = db.relationship('TestQuestion', back_populates='options')

    __table_args__ = (
        CheckConstraint('position BETWEEN 0 AND 3', name='ck_option_position_bounds'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "text": self.text,
            "isCorrect": self.is_correct
        }
