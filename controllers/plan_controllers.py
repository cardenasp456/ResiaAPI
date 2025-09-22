from flask import Blueprint, jsonify, request
from services.chat_service import ChatService
from services.llama_service import modificar_plan, make_chat_title
from models.plans_model import PlanModel
from models.encuestas_model import EncuestasModel
from services.curriculum_service import CurriculumService

# Definir un blueprint para los controladores de los planes de estudio
plan_blueprint = Blueprint('plan_blueprint', __name__)

# Ruta para consultar el plan de estudios
@plan_blueprint.route('/api/plan_estudio', methods=['GET'])
def get_plan_estudio():
    plan = PlanModel().get_plan_estudio()
    return jsonify(plan)

# Ruta para consultar las encuestas de los estudiantes
@plan_blueprint.route('/api/encuestas', methods=['GET'])
def get_encuestas():
    encuestas = EncuestasModel().get_encuestas_estudiantes()
    return jsonify(encuestas)

@plan_blueprint.route('/api/modificar_plan', methods=['POST'])
def modificar_plan_controller():
    try:
        data = request.get_json(force=True) or {}
        subject = data.get('subject')
        search = data.get('search')

        # Log visible
        print("RAW subject:", subject)
        print("RAW search:", search)

        # Normalizar tipos (defendernos de listas)
        def to_str(x):
            if isinstance(x, list):
                # Une en una sola línea legible; ajusta a tu UX si prefieres bullets
                return " | ".join(map(str, x))
            return "" if x is None else str(x)

        subject_str = to_str(subject).strip()
        search_str  = to_str(search).strip()

        if not subject_str:
            return jsonify({"error": "El campo 'subject' es obligatorio y debe ser texto."}), 400

        # Llamada al servicio LLM
        respuesta_llama = modificar_plan(subject_str, search_str)
        print("Respuesta Llama:", respuesta_llama)

        if respuesta_llama:
            chat_title = make_chat_title(subject, search)
            chat_service = ChatService()
            new_chat = chat_service.create_new_chat(chat_title)
            chat_service.save_ai_response(new_chat['chat_id'], respuesta_llama)
            return jsonify(respuesta_llama)

        return jsonify({"error": "No se pudo modificar el plan con el modelo (respuesta vacía o no válida)."}), 502

    except Exception as e:
        # No entregar 500 mudo
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Fallo interno en modificar_plan_controller", "detail": str(e)}), 500
    

@plan_blueprint.route('/curriculum', methods=['GET'])
def get_curriculum():
    course_name = request.args.get('course_name')
    grade_level = request.args.get('grade_level')

    print(course_name, grade_level)

    if not course_name or not grade_level:
        return jsonify({"message": "Se requieren los parámetros 'course_name' y 'grade_level'"}), 400

    curriculum_service = CurriculumService()
    curriculum = curriculum_service.get_curriculum(course_name, grade_level)
    if curriculum:
        return jsonify(curriculum), 200
    else:
        return jsonify({"message": "No se encontró el plan de estudio"}), 404
    
@plan_blueprint.route('/editCurriculum', methods=['POST'])
def edit_curriculum():
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar que los parámetros requeridos estén presentes
    course_name = data.get('course_name')
    grade_level = data.get('grade_level')
    updated_data = data.get('updated_data')

    if not course_name or not grade_level or not updated_data:
        return jsonify({"message": "Se requieren los parámetros 'course_name', 'grade_level' y 'updated_data'"}), 400

    # Instanciar el servicio de curriculum
    curriculum_service = CurriculumService()

    # Llamar al método para editar el curriculum
    response, status_code = curriculum_service.edit_curriculum(course_name, grade_level, updated_data)

    # Devolver la respuesta
    return jsonify(response), status_code