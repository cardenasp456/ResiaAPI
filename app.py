from flask import Flask
from flask_cors import CORS
from controllers.plan_controllers import plan_blueprint

app = Flask(__name__)
CORS(app) 

# Registrar los blueprints (controladores)
app.register_blueprint(plan_blueprint)

if __name__ == '__main__':
    app.run(debug=True)