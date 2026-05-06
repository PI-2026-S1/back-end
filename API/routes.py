from flask import Blueprint, request, jsonify
import uuid
import threading
import os
from core.processor import process_video_task
from functools import wraps

# blueprint para organizar as rotas
detection_bp = Blueprint('detection', __name__)

# temporário até que tenhamos um sistema de filas e processamento assíncrono
analysis_jobs = {}

# pasta temporária para uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# TODO implementar validação de arquivos de vídeo (tamanho, formato, etc) para evitar sobrecarga do sistema

# ─── Auth ──────────────────────────────────────────────────────────────────────

VALID_API_KEYS = set(
    key.strip()
    for key in os.environ.get("API_KEYS", "").split(",")
    if key.strip()
)
print(f"[DEBUG] API Keys carregadas: {VALID_API_KEYS}")  # remover depois

# rotas que não precisam de autenticação (com e sem prefixo do blueprint)
PUBLIC_ROUTES = {"/health", "/api/health"}

def require_api_key(f):
    """Decorator que protege uma rota com API Key."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({"error": "Missing API Key", "hint": "Provide it via X-API-Key header"}), 401

        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Invalid or unauthorized API Key"}), 403

        return f(*args, **kwargs)
    return decorated

# ─── Hooks ─────────────────────────────────────────────────────────────────────

# TODO implementar autenticação e autorização para proteger as rotas de análise
@detection_bp.before_request
def handle_before_request():
    print(f"Received {request.method} request to {request.path} from {request.remote_addr}")

    # pula auth para rotas públicas
    if request.path in PUBLIC_ROUTES:
        return

    api_key = request.headers.get("X-API-Key")

    if not api_key:
        return jsonify({"error": "Missing API Key", "hint": "Provide it via X-API-Key header"}), 401

    if api_key not in VALID_API_KEYS:
        return jsonify({"error": "Invalid or unauthorized API Key"}), 403

# ─── Rotas ─────────────────────────────────────────────────────────────────────

@detection_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@detection_bp.route('/detect', methods=['POST'])
def start_detection():
    # 1. verifica se um arquivo de vídeo foi enviado
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']

    # TODO implementar sistema de filas (ex: Celery) para processar os vídeos em background

    job_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_FOLDER, f"{job_id}.mp4")

    # 2. salva o vídeo temporariamente para processamento (pode ser otimizado para streaming direto para o processador)
    video_file.save(temp_path)

    # 3. inicializa o status no dicionário global
    analysis_jobs[job_id] = {
        "status": "processing",
        "progress": 0,
        "video_path": temp_path
    }

    # 4. inicia o processamento em background (pode ser otimizado para usar um sistema de filas real como Celery ou RQ)
    # TODO atualizar status e progresso conforme o processo avança (feito via jobs_dict no processor)
    thread = threading.Thread(
        target=process_video_task,
        args=(job_id, temp_path, analysis_jobs)
    )
    thread.start()

    # TODO armazenar resultados em banco de dados ou sistema de arquivos para consulta posterior

    return jsonify({
        "job_id": job_id,
        "status": "processing",
        "message": "Video upload successful, analysis started."
    }), 202

@detection_bp.route('/status/<job_id>', methods=['GET'])
def check_status(job_id):
    job = analysis_jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", 0)
    }), 200

@detection_bp.route('/results/<job_id>', methods=['GET'])
def get_results(job_id):
    job = analysis_jobs.get(job_id)

    # 1. verifica se o Job sequer existe
    if not job:
        return jsonify({"error": "Job not found"}), 404

    # 2. verifica se o processamento já terminou
    if job["status"] == "processing":
        return jsonify({
            "error": "Analysis still in progress",
            "job_id": job_id,
            "status": job["status"],
            "progress": job.get("progress", 0)
        }), 202

    if job["status"] == "error":
        return jsonify({
            "error": "Processing failed",
            "job_id": job_id,
            "details": job.get("error")
        }), 500

    if job["status"] == "completed":
        # 3. retorna os dados finais injetados pelo processor.py
        results = job.get("result")

        # Opcional: manter o log do job ou deletar para limpar memória
        # del analysis_jobs[job_id]

        return jsonify({
            "job_id": job_id,
            "status": "completed",
            "analysis_date": "2026-05-06T17:00:00Z", # Idealmente usar datetime.now()
            "results": results
        }), 200
