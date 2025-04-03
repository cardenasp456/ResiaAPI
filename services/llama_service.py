import requests
import json

def modificar_plan(subject, search):
    from services.curriculum_service import CurriculumService
    from services.survey_service import SurveyService
       # Instanciar el servicio de curriculum
    curriculum_service = CurriculumService()
    survey_service = SurveyService()
    # Obtener el plan de estudios y las encuestas

    plan_estudio_str = curriculum_service.get_curriculum(subject, "7"); 
    encuestas_str = survey_service.get_summary_by_subject(subject);
    
    llama_payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "assistant", "content": "Eres un experto en educación. Modifica el plan de estudios usando las encuestas ademas ten en cuenta la materia selecionada y las especificaciones del usuario."},
            {"role": "user", "content": f"Plan: {plan_estudio_str}"},
            {"role": "user", "content": f"Encuestas: {encuestas_str}"},
            {"role": "user", "content": f"Materia seleccionada: {subject}"},
            {"role": "user", "content": f"Especificaciones del usuario: {search}"}
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.7  
        }
    }
    
    try:
        llama_response = requests.post("http://localhost:11434/api/chat", json=llama_payload)
        if llama_response.status_code == 200:
            return llama_response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None


def survey_summary_calculation(self, surveys_data):
    surveys_data_str = json.dumps(surveys_data, separators=(',', ':'))
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "assistant", "content": "Eres un experto en análisis de datos. Calcula los promedios de dificultad, disfrute y participación, y determina los temas más y menos interesantes para la clase."},
            {"role": "user", "content": f"{surveys_data_str}"}  # Envía los datos de las encuestas
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.7  
        }
    }

    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la solicitud a Ollama: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None