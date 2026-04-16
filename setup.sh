#!/bin/bash

echo "=================================================="
echo "Configurando Ambiente de Detecção de Deepfakes (Unix)"
echo "=================================================="

# 1. Criar ambiente virtual
echo "Criando ambiente virtual (venv)..."
python3 -m venv venv

# 2. Ativar o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# 3. Atualizar o pip
echo "Atualizando o pip..."
pip install --upgrade pip

# 4. Instalar as dependências
if [ -f requirements.txt ]; then
    echo "Instalando dependencias do requirements.txt..."
    pip install -r requirements.txt
else
    echo "[ERRO] Arquivo requirements.txt nao encontrado!"
fi

echo "=================================================="
echo "Setup concluido!"
echo "Para comecar, use: source venv/bin/activate"
echo "Depois, execute a API com: python app.py"
echo "=================================================="