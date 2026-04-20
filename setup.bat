@echo off
echo --- Iniciando Setup do Backend (Windows) ---

:: 1. Criar ambiente virtual se não existir
if not exist venv (
    python -m venv venv
    echo [OK] Ambiente virtual criado.
) else (
    echo [INFO] Ambiente virtual ja existe.
)

:: 2. Ativar o venv e instalar dependencias
echo [INFO] Instalando dependencias...
call venv\Scripts\activate
pip install -r requirements.txt

:: 3. Configurar Git Hooks
echo [INFO] Configurando travas de seguranca do Git (pre-commit)...
pre-commit install

echo --- Setup concluido com sucesso! ---
echo Para rodar a API: python api/app.py
echo Para rodar os testes: python -m unittest discover __tests__
pause
