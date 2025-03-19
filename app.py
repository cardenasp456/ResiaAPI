from flask import Flask
from flask_cors import CORS
from database import db  # Importar la instancia de la base de datos
from controllers.survey_controllers import survey_blueprint  # Controlador para las encuestas
from controllers.plan_controllers import plan_blueprint  # Controlador para los planes de estudio

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde cualquier origen (opcional)
CORS(app)

# Configuración de la base de datos para SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DAVIDCARDE:toor@localhost/AppResia?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación Flask
db.init_app(app)

# Registrar los Blueprints
app.register_blueprint(plan_blueprint)
app.register_blueprint(survey_blueprint) 

if __name__ == '__main__':
    app.run(debug=True)