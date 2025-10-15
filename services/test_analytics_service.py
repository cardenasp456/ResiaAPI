from typing import Dict, Any
from database import db
from models.test_submission_analytics_model import (
    TestSubmissionAnalytics, TestSubmissionAnalyticsSkill
)
from models.test_submission_model import TestSubmission

def save_submission_radar(submission_id: int, radar: Dict[str, Any]) -> TestSubmissionAnalytics:
    """Guarda (o actualiza) el radar para un test_submission."""
    # Valida que exista la submission
    sub = TestSubmission.query.get(submission_id)
    if not sub:
        raise ValueError("Submission no existe.")

    # Upsert sencillo: si ya existe analytics para esta submission, lo actualizamos
    analytics = TestSubmissionAnalytics.query.filter_by(submission_id=submission_id).first()
    if not analytics:
        analytics = TestSubmissionAnalytics(submission_id=submission_id)
        db.session.add(analytics)

    # Campos principales
    skills = (radar or {}).get("skills") or []
    scale = (radar or {}).get("scale") or {}
    overall = (radar or {}).get("overall") or {}
    meta = (radar or {}).get("_meta") or {}

    analytics.source = str(meta.get("source") or "unknown")[:40]
    analytics.method = str(overall.get("method") or "mean_skills")[:40]
    try:
        analytics.overall_score = int(overall.get("score") or 0)
    except Exception:
        analytics.overall_score = 0
    try:
        analytics.scale_min = int(scale.get("min") if scale.get("min") is not None else 0)
        analytics.scale_max = int(scale.get("max") if scale.get("max") is not None else 100)
    except Exception:
        analytics.scale_min, analytics.scale_max = 0, 100

    # Limpiamos skills anteriores y reinsertamos
    analytics.skills.clear()
    for s in skills:
        name = str(s.get("name") or s.get("skill") or "").strip()[:120]
        if not name:
            continue
        try:
            score = int(round(float(s.get("score"))))
        except Exception:
            score = 0
        score = max(0, min(100, score))
        rationale = str(s.get("rationale") or s.get("explanation") or "")
        analytics.skills.append(TestSubmissionAnalyticsSkill(
            name=name, score=score, rationale=rationale
        ))

    db.session.commit()
    return analytics
