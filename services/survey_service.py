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

    def insert_survey(self, class_name, difficulty, enjoyment, engagement, topics_of_interest, comments):
        new_survey = Survey(
            class_name=class_name,
            difficulty=difficulty,
            enjoyment=enjoyment,
            engagement=engagement,
            topics_of_interest=topics_of_interest,
            comments=comments
        )
        db.session.add(new_survey)
        db.session.commit()
        return new_survey
    
    def get_all_surveys(self):
        return Survey.query.all()
    
    
    def calculate_and_update_summary(self, class_name):
        # Obtener todas las encuestas para la clase especificada
        surveys = Survey.query.filter_by(class_name=class_name).all()
        
        if not surveys:
            print(f"No se encontraron encuestas para la clase: {class_name}")
            return None

        # Preparar los datos de las encuestas para enviarlos a Ollama
        surveys_data = [survey.to_dict() for survey in surveys]
        
        # Imprimir las encuestas procesadas
        print("Datos de las encuestas:", json.dumps(surveys_data, indent=4))

        # Llamar a SurveySummaryCalculation en el servicio de Ollama
        result = self.survey_summary_calculation(surveys_data)
        if result:
            # Procesar la respuesta de Ollama
            most_interesting_topics = result.get('most_interesting_topics', [])
            least_interesting_topics = result.get('least_interesting_topics', [])
            average_difficulty = result.get('average_difficulty', 'Desconocida')
            average_enjoyment = result.get('average_enjoyment', 'Desconocida')
            average_engagement = result.get('average_engagement', 'Desconocida')

            # Actualizar o insertar en SurveySummary
            summary = SurveySummary.query.filter_by(class_name=class_name).first()
            if summary:
                summary.most_interesting_topics = json.dumps(most_interesting_topics)
                summary.least_interesting_topics = json.dumps(least_interesting_topics)
                summary.average_difficulty = average_difficulty
                summary.average_enjoyment = average_enjoyment
                summary.average_engagement = average_engagement
            else:
                summary = SurveySummary(
                    class_name=class_name,
                    most_interesting_topics=json.dumps(most_interesting_topics),
                    least_interesting_topics=json.dumps(least_interesting_topics),
                    average_difficulty=average_difficulty,
                    average_enjoyment=average_enjoyment,
                    average_engagement=average_engagement
                )
                db.session.add(summary)

            db.session.commit()
            return summary
        else:
            print("Error al procesar la respuesta de Ollama.")
            return None
