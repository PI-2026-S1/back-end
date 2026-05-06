import cv2
import os
import time
import numpy as np
import random

def preprocess_frame(frame, target_size=(224, 224)):
    """
    Prepara o frame do OpenCV para ser injetado no modelo de IA.
    """
    # Redimensionamento
    frame_resized = cv2.resize(frame, target_size)

    # Conversão de cor (OpenCV usa BGR, modelos de IA usam RGB)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # Conversão para float32 e normalização [0, 1]
    frame_normalized = frame_rgb.astype(np.float32) / 255.0

    # Expansão de dimensão: de (224, 224, 3) para (1, 224, 224, 3)
    input_tensor = np.expand_dims(frame_normalized, axis=0)

    return input_tensor

def process_video_task(job_id, video_path, jobs_dict):
    cap = None
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            jobs_dict[job_id].update({"status": "error", "error": "Could not open video file"})
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps) if fps > 0 else 1

        print(f"[*] Iniciando Job {job_id}: {total_frames} frames detectados.")

        predictions = []
        label = "real"  # valor padrão caso nenhum frame seja processado
        media = 0.0     # valor padrão

        while True:
            current_frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            ret, frame = cap.read()
            if not ret:
                break

            # Pré-processamento do frame atual
            input_data = preprocess_frame(frame, target_size=(224, 224))

            # --- ESPAÇO PARA A IA (Futuro) ---
            # score = model.predict(input_data)
            score = random.uniform(0.1, 0.9)
            predictions.append(score)

            # Atualiza o progresso
            progress = int((current_frame_idx / total_frames) * 100)
            jobs_dict[job_id]["progress"] = progress

            # Pula frames para otimizar velocidade
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_idx + frame_interval)

            time.sleep(0.01)

        # Calcula resultado final APÓS o loop terminar (não a cada frame)
        media = sum(predictions) / len(predictions) if predictions else 0.0
        label = "fake" if media > 0.5 else "real"

        # Finaliza o Job com sucesso
        jobs_dict[job_id].update({
            "status": "completed",
            "progress": 100,
            "result": {
                "label": label,
                "confidence": round(media, 2),
                "verdict": f"{label} naty",
                "message": "Analise concluida com sucesso."
            }
        })
        print(f"[+] Job {job_id} concluído com sucesso.")

    except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            jobs_dict[job_id].update({"status": "error", "error": error_msg})
            print(f"[!] Erro no Job {job_id}:\n{error_msg}")

    finally:
        # 1. Garante que o vídeo seja liberado
        if cap is not None:
            cap.release()

        # 2. Garante que o arquivo temporário seja apagado
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
                print(f"[*] Arquivo temporário removido: {video_path}")
        except Exception as cleanup_error:
            print(f"[!] Falha ao remover arquivo temporário: {cleanup_error}")
