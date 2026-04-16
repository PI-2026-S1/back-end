from flask import Flask, request, jsonify
import os
import cv2  # OpenCV para o processamento de vídeo
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'temp_videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/detectar', methods=['POST'])
def detectar_deepfake():
    # 1. Verificar se o vídeo foi enviado pelo Flutter
    if 'video' not in request.files:
        return jsonify({"erro": "Nenhum ficheiro enviado"}), 400
    
    file = request.files['video']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # 2. Chamada ao Core de Visão Computacional (Placeholder)
        # Aqui vais integrar a lógica de extração de frames e o PyTorch
        probabilidade = 0.85  # Exemplo de retorno da IA
        
        return jsonify({
            "status": "sucesso",
            "probabilidade_fake": probabilidade,
            "mensagem": "Análise concluída com sucesso"
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500