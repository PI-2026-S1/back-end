from flask import Blueprint, send_from_directory, render_template
import os

swagger_bp = Blueprint(
    "swagger",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/swagger"
)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

@swagger_bp.route("/openapi.yaml")
def openapi_spec():
    return send_from_directory(BASE_PATH, "openapi.yaml")

@swagger_bp.route("/static/<path:filename>")
def swagger_static(filename):
    return send_from_directory(os.path.join(BASE_PATH, "static"), filename)

@swagger_bp.route("/")
def docs():
    return render_template("swagger.html")
