#!/bin/bash

echo "--- Iniciando Setup do Backend ---"

# 1. Criar e ativar ambiente virtual (se não existir)
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Ambiente virtual criado."
fi

# Ativa o venv (compatível com Linux/macOS/Git Bash)
source venv/Scripts/activate || source venv/bin/activate

# 2. Instalar dependências
echo "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

# 3. Configurar Git Hooks (Pre-commit)
echo "Configurando travas de segurança do Git (pre-commit)..."
pre-commit install

echo "--- Setup concluído com sucesso! ---"
echo "Para rodar os testes: python -m unittest discover __tests__"
