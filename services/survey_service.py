import json
import requests
from models.SurveySumary_model import SurveySummary
from models.survey_model import Survey
from database import db
from services.llama_service import survey_summary_calculation

class SurveyService:
    def __init__(self):
        # Inicialización del servicio
        pass

    def insert_survey(self, student_name, subject, answers):
         # Buscar si ya existe un registro con el mismo student_name y subject
        existing_survey = Survey.query.filter_by(student_name=student_name, subject=subject).first()

        if existing_survey:
            # Si existe, actualizar los valores
            existing_survey.answers = json.dumps(answers)  # Actualizar las respuestas
            db.session.commit()
            return existing_survey
        else:
            # Si no existe, crear un nuevo registro
            new_survey = Survey(
                student_name=student_name,
                subject=subject,
                answers=json.dumps(answers)  # Convertir las respuestas a formato JSON si es necesario
            )
            db.session.add(new_survey)
            db.session.commit()
            return new_survey
    
    def get_all_surveys(self):
        return Survey.query.all()
    
    
    def calculate_and_update_summary(self, class_name):
        # Obtener todas las encuestas con el mismo subject
        surveys = Survey.query.filter_by(subject=class_name).all()

        if not surveys:
            return None  # Si no hay encuestas, devolver None

        # Inicializar una lista para acumular las respuestas por índice
        aggregated_answers = []

        for survey in surveys:
            try:
                # Cargar las respuestas desde el campo JSON
                answers = json.loads(survey.answers)
                # Expandir la lista de respuestas acumuladas si es necesario
                while len(aggregated_answers) < len(answers):
                    aggregated_answers.append([])

                # Agregar cada respuesta al índice correspondiente
                for i, answer in enumerate(answers):
                    aggregated_answers[i].append(answer)
            except json.JSONDecodeError:
                continue  # Ignorar encuestas con datos inválidos

        # Calcular el promedio por índice
        averages = []
        for index_answers in aggregated_answers:
            if index_answers:  # Verificar que haya respuestas en este índice
                averages.append(round(sum(index_answers) / len(index_answers), 2))
            else:
                averages.append(None)  # Si no hay respuestas, agregar None

        # Calcular el promedio por índice
        averages = []
        for index_answers in aggregated_answers:
            if index_answers:  # Verificar que haya respuestas en este índice
                averages.append(round(sum(index_answers) / len(index_answers), 2))
            else:
                averages.append(None)  # Si no hay respuestas, agregar None

        # Guardar los datos en SurveySummary
        summary = SurveySummary.query.filter_by(subject=class_name).first()
        if summary:
            # Actualizar el registro existente
            summary.answers = json.dumps(averages)  # Guardar los promedios como JSON
        else:
            # Crear un nuevo registro
            summary = SurveySummary(
                subject=class_name,
                answers=json.dumps(averages)  # Guardar los promedios como JSON
            )
            db.session.add(summary)

        db.session.commit()  # Confirmar los cambios en la base de datos

        return averages


    def delete_survey_by_id(self, survey_id):
        survey = Survey.query.filter_by(summary_id=survey_id).first()

        if not survey:
            return False  
        
        db.session.delete(survey)
        db.session.commit()
        return True  