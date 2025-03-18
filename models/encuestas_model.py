import json

class EncuestasModel:
    def get_encuestas_estudiantes(self):
        with open('plans/encuestas_estudiantes.json', encoding='utf-8') as f:
            encuestas = json.load(f)
        return encuestas