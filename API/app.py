from flask import Flask, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from swagger.swagger_blueprint import swagger_bp

app = Flask(__name__)

UPLOAD_FOLDER = 'temp_videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/detect', methods=['POST'])
def detectar_deepfake():
    # validação de segurança: verifica se o ficheiro existe na requisição
    if 'video' not in request.files:
        return jsonify({"erro": "Nenhum ficheiro de vídeo enviado"}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({"erro": "Nome do ficheiro vazio"}), 400

    # guarda o vídeo localmente (futuramente será no AWS)
    # uuid para evitar arquivos com o mesmo nome
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 1. Extração de Frames (OpenCV)
        # 2. Detecção Facial (MTCNN/MediaPipe)
        # 3. Inferência da Rede Neural (PyTorch)
        
        # mock
        resultado = {
            "status": "sucesso",
            "probabilidade_fake": 0.85,
            "detalhes": {
                "analise": "Fake Natty",
                "filename_processado": filename
            }
        }
        
        os.remove(filepath)
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"erro": f"Erro no processamento: {str(e)}"}), 500
    

app.register_blueprint(swagger_bp)

if __name__ == "__main__":
    print("Iniciando API de Detecção de Deepfakes...")
    print("Ouvindo em: http://0.0.0.0:5000")
    # debug=True permite que a API reinicie sozinha ao guardar alterações
    app.run(debug=True, host='0.0.0.0', port=5000)