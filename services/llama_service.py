import requests
import json

def modificar_plan(plan_estudio, encuestas, subject, search):
    plan_estudio_str = json.dumps(plan_estudio, separators=(',', ':'))
    encuestas_str = json.dumps(encuestas, separators=(',', ':'))
    
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