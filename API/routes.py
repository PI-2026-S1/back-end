from flask import Blueprint, request, jsonify
import uuid

# blueprint para organizar as rotas
detection_bp = Blueprint('detection', __name__)

# temporário até que tenhamos um sistema de filas e processamento assíncrono
analysis_jobs = {}

@detection_bp.route('/detect', methods=['POST'])
def start_detection():
    job_id = str(uuid.uuid4())
    analysis_jobs[job_id] = {"status": "processing", "progress": 0}
    
    # TODO iniciar processo de análise assíncrona
    # TODO atualizar status e progresso conforme o processo avança
    # TODO remover job da lista quando concluído
    # TODO implementar sistema de filas (ex: Celery) para processar os vídeos em background
    # TODO armazenar resultados em banco de dados ou sistema de arquivos para consulta posterior

    return jsonify({"job_id": job_id, "status": "processing"}), 202

@detection_bp.route('/status/<job_id>', methods=['GET'])
def check_status(job_id):
    job = analysis_jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"job_id": job_id, **job}), 200