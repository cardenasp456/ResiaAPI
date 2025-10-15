# controllers/test_controllers.py
from flask import Blueprint, request, jsonify
from models.student_status_test_model import StudentStatusTest
from services.tests_service import validate_payload, create_test
from database import db

tests_bp = Blueprint("tests", __name__, url_prefix="/api/tests")

@tests_bp.post("")   # <- sin slash
def create():
    data = request.get_json(silent=True, force=True)
    err = validate_payload(data)
    if err:
        return jsonify({"error": err}), 400
    try:
        test = create_test(data)
        return jsonify(test.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo guardar la prueba.", "detail": str(e)}), 500

@tests_bp.get("/")
@tests_bp.get("")      # acepta ambos
def list_tests():
    grade = request.args.get("gradeLevel")
    subject = request.args.get("subject")
    q = StudentStatusTest.query
    if grade:   q = q.filter(StudentStatusTest.grade_level == grade)
    if subject: q = q.filter(StudentStatusTest.subject == subject)
    return jsonify([t.to_dict() for t in q.order_by(StudentStatusTest.created_at.desc()).all()]), 200

@tests_bp.get("/<int:test_id>")
def get_test(test_id: int):
    test = StudentStatusTest.query.get_or_404(test_id)
    return jsonify(test.to_dict()), 200
