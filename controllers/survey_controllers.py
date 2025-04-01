from flask import Blueprint, request, jsonify
from services.survey_service import SurveyService

# Crear un Blueprint para los controladores de encuestas
survey_blueprint = Blueprint('survey_blueprint', __name__)

# Inicializar el servicio
survey_service = SurveyService()

@survey_blueprint.route('/survey', methods=['POST'])
def create_survey():
     # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()

    student_name = data.get('studentName')
    subject = data.get('subject')
    answers = data.get('answers')

    # Validar datos recibidos
    if not student_name or not subject or not answers:
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    # Insertar la encuesta utilizando el servicio
    new_survey = survey_service.insert_survey(
        student_name,
        subject,
        answers
    )

    if new_survey:
        # Calcular y actualizar el resumen
        summary = survey_service.calculate_and_update_summary(subject)
        print(summary)
        # Si la encuesta se insertó correctamente, devolver la respuesta
        return jsonify({
            "message": "Encuesta creada exitosamente"
        }), 201
    else:
        return jsonify({"message": "Error al crear la encuesta"}), 500
    

@survey_blueprint.route('/surveys', methods=['GET'])
def get_surveys():
    surveys = survey_service.get_all_surveys()
    return jsonify([survey.to_dict() for survey in surveys]), 200


@survey_blueprint.route('/deleteSurvey', methods=['POST'])
def delete_survey():
    data = request.get_json()

    subject = data.get('subject')
    survey_id = data.get('summary_id')

    success = survey_service.delete_survey_by_id(survey_id)
    if success:
        summary = survey_service.calculate_and_update_summary(subject)
        print(summary)
        return jsonify({"message": "Encuesta eliminada exitosamente"}), 200
    else:
        return jsonify({"message": "Encuesta no encontrada"}), 404