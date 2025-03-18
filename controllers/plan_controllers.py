from flask import Blueprint, jsonify, request
from services.llama_service import modificar_plan
from models.plans_model import PlanModel
from models.encuestas_model import EncuestasModel

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

# Ruta para modificar el plan de estudios según las encuestas usando Llama
@plan_blueprint.route('/api/modificar_plan', methods=['POST'])
def modificar_plan_controller():
    data = request.get_json()
    subject = data.get('subject')
    search = data.get('search')
    plan = PlanModel().get_plan_estudio()
    encuestas = EncuestasModel().get_encuestas_estudiantes()
    
    # Hacer la modificación del plan usando Llama
    respuesta_llama = modificar_plan(plan, encuestas, subject, search)
    
    if respuesta_llama:
        return jsonify(respuesta_llama)
    else:
        return jsonify({"error": "No se pudo modificar el plan con Llama"}), 500
