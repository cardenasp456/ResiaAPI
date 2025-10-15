from typing import Optional
import requests
import json
import re
import json, re, requests
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import joinedload
from database import db
from models.student_status_test_model import StudentStatusTest, TestQuestion, TestOption
from models.test_submission_model import TestSubmission

# def modificar_plan(subject, search):
#     from services.curriculum_service import CurriculumService
#     from services.survey_service import SurveyService

#     curriculum_service = CurriculumService()
#     survey_service = SurveyService()
#     # Obtener el plan de estudios y las encuestas

#     plan_estudio_str = curriculum_service.get_curriculum(subject, "7"); 
#     encuestas_str = survey_service.get_summary_by_subject(subject);
    
#     llama_payload = {
#         "model": "qwen2.5:7b-instruct",
#         "prompt": "Why is the sky blue?",   # <- corregido
#         "stream": False,                     # <- sin streaming: te devuelve todo en 'response'
#         "options": { "temperature": 0.2, "num_ctx": 4096, "num_gpu": 0 },
#         "keep_alive": 0
#     }
    
    
#     try:
#         llama_response = requests.post("http://localhost:11434/api/generate", json=llama_payload)
#         if llama_response.status_code == 200:
#             return llama_response.json()
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error en la solicitud: {e}")
#         return None

def modificar_plan(subject, search):
    import json, re, requests
    from typing import Optional, Dict, Any

    # Servicios de dominio
    from services.curriculum_service import CurriculumService
    from services.survey_service import SurveyService

    curriculum_service = CurriculumService()
    survey_service = SurveyService()

    # Normalización segura
    subject = (subject or "").strip() or "Curso"
    search  = (search or "").strip()

    # Datos base
    plan_estudio_str = curriculum_service.get_curriculum(subject, "7") or ""
    encuestas_str    = survey_service.get_summary_by_subject(subject) or ""

    # Instrucciones estrictas (también las ponemos en 'prompt' por compatibilidad)
    system_text = (
        "asistente de un colegio, experto en planes de estudio y encuestas de estudiantes. "
    )

    user_payload = {
        "Plan actual": plan_estudio_str,
        "Encuestas": encuestas_str,
        "Materia seleccionada": subject,
        "Especificaciones del usuario": search
    }

    prompt_text = (
        system_text
        + "\n\n### Datos de entrada (JSON)\n"
        + json.dumps(user_payload, ensure_ascii=False)
    )

    payload_gen = {
        "model": "qwen2.5:7b-instruct",
        "prompt": prompt_text,       
        "system": system_text,       
        "format": {
            "type": "object",
            "properties": {
                "course_name": { "type": "string", "minLength": 1 },
                "grade_level": { "type": ["string", "integer"] },
                "units": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                    "unit_name": { "type": "string", "minLength": 1 },
                    "objectives": {
                        "type": "array",
                        "minItems": 1,
                        "items": { "type": "string", "minLength": 1 }
                    },
                    "topics": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                        "type": "object",
                        "properties": {
                            "topic_name": { "type": "string", "minLength": 1 },
                            "description": { "type": "string" }
                        },
                        "required": ["topic_name"]
                        }
                    }
                    },
                    "required": ["unit_name", "objectives", "topics"]
                }
                }
            },
            "required": ["course_name", "grade_level", "units"]
            },           
        "stream": False,             
        "options": {
            "temperature": 1,
            "num_ctx": 20096,
            "stop": ["```"]         
        },
        "keep_alive": 0              
    }

    # Helper: extraer JSON con llaves balanceadas, por si el modelo agregara ruido
    def extract_balanced_json(text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
        start = s.find("{")
        if start == -1:
            return None
        stack = 0; in_str = False; esc = False; end = -1
        for i in range(start, len(s)):
            ch = s[i]
            if in_str:
                if esc: esc = False
                elif ch == "\\": esc = True
                elif ch == '"': in_str = False
            else:
                if ch == '"': in_str = True
                elif ch == '{': stack += 1
                elif ch == '}':
                    stack -= 1
                    if stack == 0:
                        end = i
                        break
        if end == -1:
            return None
        candidate = s[start:end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # reparación mínima (coma colgante)
            candidate2 = re.sub(r",\s*([}\]])", r"\1", candidate)
            try:
                return json.loads(candidate2)
            except json.JSONDecodeError:
                return None

    # Llamada a Ollama
    try:
        r = requests.post("http://localhost:11434/api/generate", json=payload_gen, timeout=120)
        if r.status_code != 200:
            print("[qwen/generate] HTTP", r.status_code, r.text[:600])
            raise RuntimeError("HTTP non-200 en generate")

        data = r.json()
        content = data.get("response", "")

        # Con format=json debería venir limpio; si no, intentamos extraer
        parsed = None
        if content:
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                parsed = extract_balanced_json(content)

        # Validación mínima
        if parsed and isinstance(parsed.get("units"), list) and parsed.get("course_name"):
            parsed["grade_level"] = str(parsed.get("grade_level", "7"))
            return parsed

        print("[qwen/generate] JSON inválido o vacío. RAW:", str(content)[:600])

    except requests.RequestException as e:
        print("[qwen/generate] Error de red:", e)
    except Exception as e:
        print("[qwen/generate] Error:", e)

    # Fallback: esqueleto mínimo para no romper flujo
    return {
        "course_name": subject,
        "grade_level": "7",
        "units": [
            {
                "unit_name": "Unidad 1",
                "objectives": ["Objetivo inicial (ajustar tras revisar disponibilidad del modelo)."],
                "topics": [
                    {"topic_name": "Tema inicial", "description": "Fallback ante respuesta vacía del modelo."}
                ]
            }
        ]
    }



def survey_summary_calculation(self, surveys_data):
    surveys_data_str = json.dumps(surveys_data, separators=(',', ':'))
    payload = {
        "model": "qwen2.5:7b-instruct",
        "prompt": [
            {"role": "assistant", "content": "a partir de las encuestas adjuntas calcula los promedios de dificultad, disfrute y participación, y determina los temas más y menos interesantes para la clase."},
            {"role": "user", "content": f"{surveys_data_str}"}  # Envía los datos de las encuestas
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.7  
        }
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la solicitud a Ollama: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None
def _fallback_title(subject: str, search: str) -> str:
    subject = (subject or "").strip()
    search = (search or "").strip()
    if not subject and not search:
        return "Nuevo chat"

    base_text = search
    if subject and not re.search(rf"^\s*{re.escape(subject)}\b", search, flags=re.IGNORECASE):
        base_text = f"{subject}: {search}" if search else subject

    words = re.findall(r"\w+[\wáéíóúüñÁÉÍÓÚÜÑ]*", base_text, flags=re.UNICODE)
    draft = " ".join(words[:6]).strip() or base_text
    title = draft[:60].rstrip()
    if title and title[0].islower():
        title = title[0].upper() + title[1:]
    if title.endswith("."):
        title = title[:-1]
    return title or "Nuevo chat"


def make_chat_title(subject: str, search: str) -> str:
    subject = (subject or "").strip()
    search = (search or "").strip()
    if not subject and not search:
        return "Nuevo chat"

    prompt = f"""
Eres un generador de títulos para hilos de chat educativos.
Con la asignatura y la búsqueda del usuario, crea UN (1) título breve y descriptivo.

Datos:
- Asignatura: "{subject}"
- Búsqueda: "{search}"
""".strip()

    payload = {
        "model": "qwen2.5:7b-instruct",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 1,
            "num_ctx": 2096,
            "stop": ["```"]          
        },
        "keep_alive": 0  
    }

    try:
        r = requests.post("http://localhost:11434/api/generate", json=payload)
        print("Respuesta make_chat_title:", r)
        if r.status_code != 200:
            return _fallback_title(subject, search)

        print("Respuesta make_chat_title:", r)
        data = r.json()
        raw = (data.get("response") or "").strip()

        title = None
        if raw:
            try:
                obj = json.loads(raw)
                title = (obj.get("title") or "").strip()
            except Exception:
                title = raw.strip()

        if not title:
            return _fallback_title(subject, search)

        title = re.sub(r"[\r\n]+", " ", title)
        title = re.sub(r"\s+", " ", title).strip().strip('"\'')

        if len(title) > 60:
            title = title[:57].rstrip() + "…"
        if title and title[0].islower():
            title = title[0].upper() + title[1:]
        if title.endswith("."):
            title = title[:-1]

        return title or _fallback_title(subject, search)
    except requests.exceptions.RequestException:
        return _fallback_title(subject, search)
    

def _extract_balanced_json(text: str) -> Optional[Dict[str, Any]]:
    """Intenta extraer el primer bloque JSON con llaves balanceadas (por si el modelo añade ruido)."""
    if not text:
        return None
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    start = s.find("{")
    if start == -1:
        return None
    stack = 0; in_str = False; esc = False; end = -1
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
        else:
            if ch == '"': in_str = True
            elif ch == '{': stack += 1
            elif ch == '}':
                stack -= 1
                if stack == 0:
                    end = i
                    break
    if end == -1:
        return None
    candidate = s[start:end+1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        candidate2 = re.sub(r",\s*([}\]])", r"\1", candidate)
        try:
            return json.loads(candidate2)
        except json.JSONDecodeError:
            return None

def _clean_skills(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normaliza skills: name:str, score:int [0..100], rationale:str (opcional). Mínimo 5."""
    out: List[Dict[str, Any]] = []
    seen = set()
    for s in skills or []:
        name = str(s.get("name") or s.get("skill") or "").strip()[:60]
        if not name:
            continue
        if name.lower() in seen:
            continue
        try:
            score = int(round(float(s.get("score", 0))))
        except Exception:
            score = 0
        score = max(0, min(100, score))
        rationale = str(s.get("rationale") or s.get("explanation") or "")[:300]
        out.append({"name": name, "score": score, "rationale": rationale})
        seen.add(name.lower())
    # garantizar mínimo 5
    while len(out) < 5:
        out.append({"name": f"Dimensión {len(out)+1}", "score": 0, "rationale": ""})
    return out[:8]  # límite superior razonable

def _fallback_radar(accuracy_percent: int) -> Dict[str, Any]:
    """Por si falla Ollama: devuelve 5 dimensiones derivadas del acierto global."""
    dims = [
        ("Comprensión de enunciados", accuracy_percent),
        ("Razonamiento lógico", accuracy_percent),
        ("Cálculo/Procedimientos", accuracy_percent),
        ("Atención al detalle", accuracy_percent),
        ("Aplicación de conceptos", accuracy_percent),
    ]
    return {
        "skills": [{"name": n, "score": int(accuracy_percent), "rationale": "Estimación por fallback"} for n, _ in dims],
        "scale": {"min": 0, "max": 100},
        "overall": {"score": int(accuracy_percent), "method": "fallback_mean"}
    }

def _compose_questions_payload(test: StudentStatusTest, submission: TestSubmission) -> List[Dict[str, Any]]:
    answers_by_q = {a.question_id: int(a.chosen_index) for a in submission.answers}
    items: List[Dict[str, Any]] = []
    for q in sorted(test.questions, key=lambda x: x.position):
        correct_idx = next((o.position for o in q.options if o.is_correct), None)
        items.append({
            "position": int(q.position),
            "questionId": int(q.id),
            "statement": q.statement,
            "options": [
                {"position": int(o.position), "text": o.text}
                for o in sorted(q.options, key=lambda k: k.position)
            ],
            "correctIndex": int(correct_idx) if correct_idx is not None else None,
            "studentIndex": answers_by_q.get(int(q.id), -1)
        })
    return items

def build_radar_for_submission(submission_id: int) -> Dict[str, Any]:
    """
    Carga la submission + test, llama a Ollama y devuelve un dict:
    { skills:[{name,score,rationale}], scale:{min,max}, overall:{score,method} }
    """
    sub: TestSubmission = (
        TestSubmission.query
        .options(db.joinedload(TestSubmission.answers))
        .get(submission_id)
    )
    if not sub:
        raise ValueError("Submission no existe.")

    test: StudentStatusTest = (
        StudentStatusTest.query
        .options(
            joinedload(StudentStatusTest.questions)
            .joinedload(TestQuestion.options)
        )
        .get(sub.test_id)
    )
    if not test:
        raise ValueError("Prueba no existe para la submission.")

    q_items = _compose_questions_payload(test, sub)
    # acierto global por si necesitamos fallback
    acc = 0
    total = len(q_items)
    for i in q_items:
        if i.get("studentIndex", -1) == i.get("correctIndex", -2):
            acc += 1
    accuracy_percent = int(round((acc / max(1, total)) * 100))

    system_text = (
        "Eres un asesor pedagógico. Debes analizar preguntas de una prueba y las respuestas "
        "de un estudiante, y producir al menos 5 dimensiones (habilidades) evaluadas con puntajes 0–100."
        " Devuelve exclusivamente JSON que cumpla el esquema."
    )

    user_payload = {
        "subject": test.subject,
        "grade_level": test.grade_level,
        "questions": q_items,
        "instructions": (
            "Crea entre 5 y 8 dimensiones (por ejemplo: Comprensión de enunciados, Razonamiento lógico, "
            "Cálculo/Procedimientos, Modelación, Comunicación, Atención al detalle). "
            "Asigna a cada dimensión un puntaje 0–100 en base a las evidencias de aciertos/errores "
            "y el contenido de los enunciados. Incluye breve justificación por dimensión."
        )
    }

    payload_gen = {
        "model": "qwen2.5:7b-instruct",
        "prompt": (
            system_text
            + "\n\n### Datos de entrada (JSON)\n"
            + json.dumps(user_payload, ensure_ascii=False)
        ),
        "system": system_text,
        "format": {
            "type": "object",
            "properties": {
                "skills": {
                    "type": "array",
                    "minItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": { "type": "string", "minLength": 2 },
                            "score": { "type": "number", "minimum": 0, "maximum": 100 },
                            "rationale": { "type": "string" }
                        },
                        "required": ["name", "score"]
                    }
                },
                "scale": {
                    "type": "object",
                    "properties": {
                        "min": { "type": "number" },
                        "max": { "type": "number" }
                    }
                },
                "overall": {
                    "type": "object",
                    "properties": {
                        "score": { "type": "number" },
                        "method": { "type": "string" }
                    }
                }
            },
            "required": ["skills"]
        },
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_ctx": 8192,
            "stop": ["```"]
        },
        "keep_alive": 0
    }

    try:
        r = requests.post("http://localhost:11434/api/generate", json=payload_gen, timeout=90)
        r.raise_for_status()
        data = r.json()
        content = data.get("response") or ""
        parsed = None
        if content:
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                parsed = _extract_balanced_json(content)

        # Normaliza y valida
        if not parsed or not isinstance(parsed.get("skills"), list):
            return {**_fallback_radar(accuracy_percent), "_meta": {"source": "fallback_no_json"}}

        skills = _clean_skills(parsed.get("skills"))
        overall = parsed.get("overall") or {"score": int(round(sum(s["score"] for s in skills) / len(skills))), "method": "mean_skills"}
        scale = parsed.get("scale") or {"min": 0, "max": 100}

        return {"skills": skills, "overall": overall, "scale": scale, "_meta": {"source": "ollama"}}

    except Exception as e:
        # Nunca romper el endpoint por fallas del modelo
        return {**_fallback_radar(accuracy_percent), "_meta": {"source": "fallback_error", "detail": str(e)}}