# Deepfake Detection System - Back-end

Este repositorio contem o nucleo de processamento e a API do projeto de deteccao de videos sinteticos (Deepfakes).

## Tecnologias e Frameworks

* **Linguagem:** Python 3.12 (Versao selecionada para compatibilidade com bibliotecas de IA).
* **Framework Web:** Flask (Arquitetura baseada em Blueprints).
* **Documentacao:** Flasgger (OpenAPI/Swagger).
* **Processamento de Imagem:** OpenCV.
* **Qualidade de Codigo:** Pre-commit Hooks (Linting e Testes).
* **CI/CD:** GitHub Actions (Integracao Continua).

## Estrutura do Projeto

O projeto esta organizado de forma a separar a interface de comunicacao da logica de processamento:

```text
back-end/
├── API/
│   ├── __tests__/      # Testes de integracao das rotas
│   ├── swagger/        # Blueprint e configuracoes da documentacao
│   ├── app.py          # Ponto de entrada da aplicacao
│   └── routes.py       # Definicao dos endpoints da API
├── core/
│   └── processor.py    # Logica de processamento de video e inferencia
├── .github/workflows/  # Pipelines de CI do GitHub Actions
├── setup.bat           # Script de instalacao automatica para Windows
├── setup.sh            # Script de instalacao automatica para Linux/macOS
└── requirements.txt    # Gerenciamento de dependencias
