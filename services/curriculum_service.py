from models.course_model import Course
from models.unit_model import Unit
from models.unitObjetive_model import UnitObjective
from models.topic_model import Topic
from models.topicContent_model import TopicContent
from models.topicAssessment_model import TopicAssessment
from models.unitResource_model import UnitResource
from database import db

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
            print(unit_data["objectives"])
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
    
    def edit_curriculum(self, course_name, grade_level, updated_data):
        # Obtener el curso por nombre y nivel de grado
        course = Course.query.filter_by(course_name=course_name, grade_level=grade_level).first()
        if not course:
            return {"message": "Curso no encontrado"}, 404
        
        # Actualizar el nombre del curso y el nivel de grado si están en los datos actualizados
        if "course_name" in updated_data:
            print("actualizando nombre del curso")
            course.course_name = updated_data["course_name"]
        if "grade_level" in updated_data:
            print("actualizando nivel de grado")
            course.grade_level = updated_data["grade_level"]
        # Actualizar las unidades
        if "units" in updated_data:
            print("actualizando unidades")
            for updated_unit in updated_data["units"]:
                unit = Unit.query.filter_by(unit_name=updated_unit["unit_name"], course_id=course.course_id).first()
                if not unit:
                    # Crear una nueva unidad si no existe
                    unit = Unit(unit_name=updated_unit["unit_name"], course_id=course.course_id)
                    db.session.add(unit)

                # Actualizar los objetivos de la unidad
                if "objectives" in updated_unit:
                    # Eliminar objetivos existentes
                    UnitObjective.query.filter_by(unit_id=unit.unit_id).delete()
                    # Agregar nuevos objetivos
                    for objective_text in updated_unit["objectives"]:
                        objective = UnitObjective(unit_id=unit.unit_id, objective_text=objective_text)
                        db.session.add(objective)

                # Actualizar los temas de la unidad
                if "topics" in updated_unit:
                    for updated_topic in updated_unit["topics"]:
                        topic = Topic.query.filter_by(topic_name=updated_topic["topic_name"], unit_id=unit.unit_id).first()
                        if not topic:
                            # Crear un nuevo tema si no existe
                            topic = Topic(topic_name=updated_topic["topic_name"], unit_id=unit.unit_id)
                            db.session.add(topic)

                        # Actualizar el contenido del tema
                        if "content" in updated_topic:
                            # Eliminar contenido existente
                            TopicContent.query.filter_by(topic_id=topic.topic_id).delete()
                            # Agregar nuevo contenido
                            for content_text in updated_topic["content"]:
                                content = TopicContent(topic_id=topic.topic_id, content_text=content_text)
                                db.session.add(content)

                        # Actualizar los métodos de evaluación del tema
                        if "assessment_methods" in updated_topic:
                            # Eliminar métodos de evaluación existentes
                            TopicAssessment.query.filter_by(topic_id=topic.topic_id).delete()
                            # Agregar nuevos métodos de evaluación
                            for assessment_method in updated_topic["assessment_methods"]:
                                assessment = TopicAssessment(topic_id=topic.topic_id, assessment_method=assessment_method)
                                db.session.add(assessment)

                # Actualizar los recursos de la unidad
                if "resources" in updated_unit:
                    # Eliminar recursos existentes
                    UnitResource.query.filter_by(unit_id=unit.unit_id).delete()
                    # Agregar nuevos recursos
                    for resource_name in updated_unit["resources"]:
                        resource = UnitResource(unit_id=unit.unit_id, resource_name=resource_name)
                        db.session.add(resource)

        # Confirmar los cambios en la base de datos
        db.session.commit()
        print("Cambios guardados en la base de datos")
        return {"message": "Plan de estudio actualizado exitosamente"}, 200