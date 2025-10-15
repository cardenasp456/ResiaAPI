# controllers/test_submission_controllers.py
from flask import Blueprint, request, jsonify
from database import db
from models.student_status_test_model import StudentStatusTest
from models.test_submission_analytics_model import TestSubmissionAnalytics
from services.llama_service import build_radar_for_submission
from services.test_analytics_service import save_submission_radar
from services.test_submissions_service import validate_submission, create_submission
from models.test_submission_model import TestSubmission

submissions_bp = Blueprint("test_submissions", __name__, url_prefix="/api/test-submissions")
submissions_bp.strict_slashes = False


@submissions_bp.post("/")
@submissions_bp.post("")
def submit_test():
    data = request.get_json(silent=True, force=True)
    err = validate_submission(data)
    if err:
        return jsonify({"error": err}), 400

    try:
        s = create_submission(data)

        # 1) Genera radar (Ollama o fallback)
        radar = build_radar_for_submission(s.id)

        # 2) Persiste radar asociado a la submission
        analytics_row = save_submission_radar(s.id, radar)

        # 3) Respuesta combinada
        resp = s.to_dict()
        resp["analytics"] = {"radar": analytics_row.to_dict()}
        return jsonify(resp), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo registrar el intento.", "detail": str(e)}), 400
    

# GET /api/test-submissions?studentId=&subject=&gradeLevel=&page=&pageSize=
@submissions_bp.get("/")
@submissions_bp.get("")
def list_submissions():
    student_id = (request.args.get("studentId") or "").strip()
    subject    = (request.args.get("subject") or "").strip()
    grade      = (request.args.get("gradeLevel") or "").strip()

    page = max(int(request.args.get("page", 1)), 1)
    page_size = min(max(int(request.args.get("pageSize", 20)), 1), 100)

    q = (
        db.session.query(TestSubmission, StudentStatusTest, TestSubmissionAnalytics)
        .join(StudentStatusTest, TestSubmission.test_id == StudentStatusTest.id)
        .outerjoin(TestSubmissionAnalytics, TestSubmissionAnalytics.submission_id == TestSubmission.id)
    )

    if student_id:
        q = q.filter(TestSubmission.student_id == student_id)
    if subject:
        q = q.filter(StudentStatusTest.subject == subject)
    if grade:
        q = q.filter(StudentStatusTest.grade_level == grade)

    total = q.count()
    rows = (
        q.order_by(TestSubmission.created_at.desc())
         .offset((page - 1) * page_size)
         .limit(page_size)
         .all()
    )

    def row_to_dict(s: TestSubmission, t: StudentStatusTest, a: TestSubmissionAnalytics):
        return {
            "id": s.id,
            "studentId": s.student_id,
            "createdAt": s.created_at,
            "score": s.score,
            "totalQuestions": s.total_questions,
            "test": {
                "id": t.id, "title": t.title, "gradeLevel": t.grade_level, "subject": t.subject
            },
            "analytics": {
                "overallScore": a.overall_score if a else None
            }
        }

    items = [row_to_dict(s, t, a) for (s, t, a) in rows]
    return jsonify({"items": items, "total": total, "page": page, "pageSize": page_size}), 200

# GET detalle de una submission (con analytics persistidas)
@submissions_bp.get("/<int:submission_id>")
def get_submission(submission_id: int):
    s: TestSubmission = TestSubmission.query.get_or_404(submission_id)
    r = s.to_dict()
    analytics = TestSubmissionAnalytics.query.filter_by(submission_id=submission_id).first()
    if analytics:
        r.setdefault("analytics", {})["radar"] = analytics.to_dict()
    return jsonify(r), 200