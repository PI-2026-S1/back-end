@echo off
echo ==================================================
echo Configurando Ambiente de Detecção de Deepfakes
echo ==================================================

:: 1. Criar ambiente virtual para não poluir o Python global
echo Criando ambiente virtual (venv)...
python -m venv venv

:: 2. Ativar o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate

:: 3. Atualizar o pip
echo Atualizando o pip...
python -m pip install --upgrade pip

:: 4. Instalar as dependências do projeto
if exist requirements.txt (
    echo Instalando dependencias do requirements.txt...
    pip install -r requirements.txt
) else (
    echo [ERRO] Arquivo requirements.txt nao encontrado!
)

echo ==================================================
echo Setup concluido! Para comecar, use: call venv\Scripts\activate
echo Depois, execute a API com: python app.py
echo ==================================================
pause