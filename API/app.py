from flask import Flask
from flasgger import Swagger
from routes import detection_bp
from swagger.swagger_blueprint import swagger_bp

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(detection_bp, url_prefix='/api')
app.register_blueprint(swagger_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1234)
