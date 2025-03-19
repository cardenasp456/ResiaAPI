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

    class_name = data.get('class_name')
    difficulty = data.get('difficulty')
    enjoyment = data.get('enjoyment')
    engagement = data.get('engagement')
    topics_of_interest = data.get('topics_of_interest')
    comments = data.get('comments')

    # Validar datos recibidos
    if not class_name or not difficulty or not enjoyment or not engagement or not topics_of_interest:
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    # Insertar la encuesta utilizando el servicio
    new_survey = survey_service.insert_survey(
        class_name,
        difficulty,
        enjoyment,
        engagement,
        topics_of_interest,
        comments
    )

    if new_survey:
        # Calcular y actualizar el resumen
        # summary = survey_service.calculate_and_update_summary(class_name)

        # Si la encuesta se insertó correctamente, devolver la respuesta
        return jsonify({
            "message": "Encuesta creada exitosamente"
        }), 201
    else:
        return jsonify({"message": "Error al crear la encuesta"}), 500