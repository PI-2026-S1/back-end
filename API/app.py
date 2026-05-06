from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv  # adiciona
from API.routes import detection_bp
from API.swagger.swagger_blueprint import swagger_bp

load_dotenv()  # adiciona — carrega o .env antes de tudo

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(detection_bp, url_prefix='/api')
app.register_blueprint(swagger_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1234)
