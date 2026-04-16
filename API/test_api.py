import requests

url = 'http://127.0.0.1:5000/api/detect'
video_path = 'video_teste.mp4' 

try:
    with open(video_path, 'rb') as video_file:
        # o dicionário deve ter a chave 'video' para bater com o request.files['video'] do Flask
        files = {'video': video_file}
        
        print(f"Enviando {video_path} para análise...")
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("Sucesso!")
            print("Resultado da IA:", response.json())
        else:
            print(f"Erro {response.status_code}: {response.text}")

except FileNotFoundError:
    print(f"Erro: O arquivo {video_path} não foi encontrado. Coloque um vídeo chamado 'video_teste.mp4' na pasta.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")