from sqlalchemy import func
from database import db
from datetime import datetime

class TestSubmissionAnalytics(db.Model):
    __tablename__ = 'test_submission_analytics'
    # __table_args__ = {'schema': 'dbo'}  # <- descomenta si usas esquema dbo fijo

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(
        db.Integer,
        db.ForeignKey('test_submissions.id', ondelete='CASCADE'),
        nullable=False, index=True
    )
    source = db.Column(db.String(40), nullable=True)          # 'ollama' | 'fallback_*'
    method = db.Column(db.String(40), nullable=True)          # p.ej. 'mean_skills'
    overall_score = db.Column(db.Integer, nullable=True)      # 0..100
    scale_min = db.Column(db.Integer, nullable=True)          # normalmente 0
    scale_max = db.Column(db.Integer, nullable=True)          # normalmente 100
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    skills = db.relationship(
        'TestSubmissionAnalyticsSkill',
        back_populates='analytics',
        cascade='all, delete-orphan',
        order_by='TestSubmissionAnalyticsSkill.id'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "submissionId": self.submission_id,
            "source": self.source,
            "method": self.method,
            "overall": {"score": self.overall_score},
            "scale": {"min": self.scale_min, "max": self.scale_max},
            "skills": [s.to_dict() for s in self.skills],
            "createdAt": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at)
        }

class TestSubmissionAnalyticsSkill(db.Model):
    __tablename__ = 'test_submission_analytics_skills'
    # __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    analytics_id = db.Column(
        db.Integer,
        db.ForeignKey('test_submission_analytics.id', ondelete='CASCADE'),
        nullable=False, index=True
    )
    name = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)             # 0..100
    rationale = db.Column(db.Text, nullable=True)

    analytics = db.relationship('TestSubmissionAnalytics', back_populates='skills')

    def to_dict(self):
        return {"name": self.name, "score": self.score, "rationale": self.rationale or ""}
