# models/test_submission_model.py
from datetime import datetime
from sqlalchemy import func, CheckConstraint
from database import db

class TestSubmission(db.Model):
    __tablename__ = 'test_submissions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('student_status_tests.id', ondelete='CASCADE'), nullable=False, index=True)
    student_id = db.Column(db.String(64), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 0..100
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    answers = db.relationship('TestSubmissionAnswer', back_populates='submission', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "testId": self.test_id,
            "studentId": self.student_id,
            "totalQuestions": self.total_questions,
            "correctAnswers": self.correct_answers,
            "score": self.score,
            "createdAt": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            "details": [a.to_dict() for a in self.answers]
        }

class TestSubmissionAnswer(db.Model):
    __tablename__ = 'test_submission_answers'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('test_submissions.id', ondelete='CASCADE'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('test_questions.id', ondelete='CASCADE'), nullable=False, index=True)
    chosen_index = db.Column(db.Integer, nullable=False)   # 0..3
    correct_index = db.Column(db.Integer, nullable=False)  # 0..3
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    submission = db.relationship('TestSubmission', back_populates='answers')

    __table_args__ = (
        CheckConstraint('chosen_index BETWEEN 0 AND 3', name='ck_chosen_bounds'),
        CheckConstraint('correct_index BETWEEN 0 AND 3', name='ck_correct_bounds'),
    )

    def to_dict(self):
        return {
            "questionId": self.question_id,
            "chosen": self.chosen_index,
            "correct": self.correct_index,
            "isCorrect": self.is_correct
        }
