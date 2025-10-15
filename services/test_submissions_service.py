# services/test_submissions_service.py
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import joinedload
from database import db
from models.student_status_test_model import StudentStatusTest, TestQuestion
from models.test_submission_model import TestSubmission, TestSubmissionAnswer

def validate_submission(data: Dict[str, Any]) -> Optional[str]:
    if not isinstance(data, dict):
        return "Body inválido."
    if not (sid := (data.get("studentId") or "").strip()):
        return "studentId es requerido."
    test_id = data.get("testId")
    if not isinstance(test_id, int):
        return "testId inválido."
    answers = data.get("answers")
    if not isinstance(answers, list) or not answers:
        return "answers debe ser un arreglo no vacío."
    if any((not isinstance(a, int) or a < 0 or a > 3) for a in answers):
        return "Cada answer debe ser entero entre 0 y 3."
    return None

def create_submission(data: Dict[str, Any]) -> TestSubmission:
    test: StudentStatusTest = (
        StudentStatusTest.query
        .options(
            joinedload(StudentStatusTest.questions).joinedload(TestQuestion.options)
        )
        .get(data["testId"])
    )
    if not test:
        raise ValueError("La prueba no existe.")

    # Ordenar preguntas por position
    qs = sorted(test.questions, key=lambda q: q.position)
    answers: List[int] = data["answers"]
    if len(answers) != len(qs):
        raise ValueError("Cantidad de respuestas no coincide con preguntas.")

    correct = 0
    submission = TestSubmission(
        test_id=test.id,
        student_id=data["studentId"].strip(),
        total_questions=len(qs),
        correct_answers=0,
        score=0
    )
    db.session.add(submission)

    for i, q in enumerate(qs):
        # correctIndex = position del option con is_correct = True
        correct_idx = next((o.position for o in q.options if o.is_correct), None)
        if correct_idx is None:
            raise ValueError(f"Pregunta {i+1} no tiene opción correcta configurada.")

        chosen = int(answers[i])
        is_ok = (chosen == int(correct_idx))
        if is_ok:
            correct += 1

        db.session.add(TestSubmissionAnswer(
            submission=submission,
            question_id=q.id,
            chosen_index=chosen,
            correct_index=int(correct_idx),
            is_correct=is_ok
        ))

    submission.correct_answers = correct
    submission.score = round((correct / max(1, len(qs))) * 100)

    db.session.commit()
    return submission
