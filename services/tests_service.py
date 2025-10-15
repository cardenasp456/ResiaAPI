# services/tests_service.py
from typing import Dict, Any, Optional
from database import db
from models.student_status_test_model import StudentStatusTest, TestQuestion, TestOption

MAX_QUESTIONS = 10
OPTIONS_PER_QUESTION = 4

def validate_payload(data: Dict[str, Any]) -> Optional[str]:
    if not isinstance(data, dict):
        return "Body inválido."

    title = (data.get("title") or "").strip()
    grade = data.get("gradeLevel")
    subject = data.get("subject")
    questions = data.get("questions")

    if not title:
        return "El título es requerido."
    if not grade:
        return "El grado (gradeLevel) es requerido."
    if not subject:
        return "La asignatura (subject) es requerida."
    if not isinstance(questions, list) or len(questions) == 0:
        return "Debe enviar al menos una pregunta."
    if len(questions) > MAX_QUESTIONS:
        return f"Máximo {MAX_QUESTIONS} preguntas."

    for qi, q in enumerate(questions):
        if not isinstance(q, dict):
            return f"Pregunta {qi+1}: formato inválido."
        statement = (q.get("statement") or "").strip()
        options = q.get("options")
        correct_index = q.get("correctIndex")
        if not statement:
            return f"Pregunta {qi+1}: el enunciado es requerido."
        if not isinstance(options, list) or len(options) != OPTIONS_PER_QUESTION:
            return f"Pregunta {qi+1}: deben existir exactamente {OPTIONS_PER_QUESTION} opciones."
        if not all((isinstance(o, str) and o.strip()) for o in options):
            return f"Pregunta {qi+1}: todas las opciones deben tener texto."
        if not isinstance(correct_index, int) or not (0 <= correct_index < OPTIONS_PER_QUESTION):
            return f"Pregunta {qi+1}: correctIndex debe estar entre 0 y {OPTIONS_PER_QUESTION-1}."

    return None

def create_test(data: Dict[str, Any]) -> StudentStatusTest:
    """Crea y persiste la prueba con sus preguntas/opciones."""
    test = StudentStatusTest(
        title=data["title"].strip(),
        grade_level=data["gradeLevel"],
        subject=data["subject"]
    )
    db.session.add(test)

    for pos_q, q in enumerate(data["questions"]):
        question = TestQuestion(
            test=test,
            position=pos_q,
            statement=q["statement"].strip()
        )
        db.session.add(question)

        correct_idx = q["correctIndex"]
        for pos_o, opt_text in enumerate(q["options"]):
            opt = TestOption(
                question=question,
                position=pos_o,
                text=opt_text.strip(),
                is_correct=(pos_o == correct_idx)
            )
            db.session.add(opt)

    db.session.commit()
    return test
