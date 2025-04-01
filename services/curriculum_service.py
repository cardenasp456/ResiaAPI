from models.course_model import Course
from models.unit_model import Unit
from models.unitObjetive_model import UnitObjective
from models.topic_model import Topic
from models.topicContent_model import TopicContent
from models.topicAssessment_model import TopicAssessment
from models.unitResource_model import UnitResource

class CurriculumService:

    def __init__(self):
        # Inicialización del servicio
        pass

    def get_curriculum(self, course_name, grade_level):
        # Obtener el curso por nombre y nivel de grado
        course = Course.query.filter_by(course_name=course_name, grade_level=grade_level).first()
        if not course:
            return None  # Si no se encuentra el curso, devolver None

        curriculum = {
            "course_name": course.course_name,
            "grade_level": course.grade_level,
            "units": []
        }

        # Iterar sobre las unidades del curso
        for unit in course.units:
            unit_data = {
                "unit_name": unit.unit_name,
                "objectives": [],
                "topics": []
            }

            # Agregar objetivos de la unidad
            unit_data["objectives"] = [objective.objective_text for objective in unit.objectives]

            # Iterar sobre los temas de la unidad
            for topic in unit.topics:
                topic_data = {
                    "topic_name": topic.topic_name,
                    "content": [],
                    "assessment_methods": []
                }

                # Agregar contenido del tema
                topic_data["content"] = [content.content_text for content in topic.contents]

                # Agregar métodos de evaluación del tema
                topic_data["assessment_methods"] = [assessment.assessment_method for assessment in topic.assessments]

                unit_data["topics"].append(topic_data)

            # Agregar recursos de la unidad
            unit_data["resources"] = [resource.resource_name for resource in unit.resources]

            curriculum["units"].append(unit_data)

        return curriculum