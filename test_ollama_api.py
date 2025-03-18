import requests
import json

# Cargar el plan de estudios
with open('plan_estudio.json', encoding='utf-8') as f:
    plan_estudio = json.load(f)

# Cargar las encuestas de los estudiantes
with open('encuestas_estudiantes.json', encoding='utf-8') as f:
    encuestas_estudiantes = json.load(f)

# Convertir ambos a strings JSON
plan_estudio_str = json.dumps(plan_estudio)
encuestas_estudiantes_str = json.dumps(encuestas_estudiantes)

# Payload para enviar al modelo
payload = {
    "model": "llama3.2",
    "messages": [
        {"role": "assistant", "content": "Eres un experto en educación. Aquí tienes un plan de estudios y encuestas de los estudiantes. Usa la información de las encuestas para modificar el plan de estudios."},
        {"role": "user", "content": f"Plan de estudios: {plan_estudio_str}"},
        {"role": "user", "content": f"Encuestas de estudiantes: {encuestas_estudiantes_str}"}
    ],
    "format": "json",
    "stream": False,
    "options": {
        "temperature": 0.7
    }
}

# Enviar la solicitud
response = requests.post(
    "http://localhost:11434/api/chat",
    json=payload
)

# Imprimir la respuesta del modelo
print(response.json())
