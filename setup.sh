#!/bin/bash

echo "--- Iniciando Setup do Backend ---"

# 1. Criar ambiente virtual usando python3
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Erro ao criar ambiente virtual. Verifique se o python3 está instalado."
        exit 1
    fi
    echo "Ambiente virtual criado."
fi

# 2. Ativa o venv (focando no padrão Unix/macOS)
source venv/bin/activate

# Atualiza o pip dentro do venv para evitar avisos
pip install --upgrade pip

# 3. Instalar dependências
echo "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

# 4. Configurar Git Hooks
# Usamos 'python -m pre_commit' caso o binário não esteja no PATH imediatamente
echo "Configurando travas de segurança do Git (pre-commit)..."
pip install pre-commit
pre-commit install

echo "--- Setup concluído com sucesso! ---"
echo "Para rodar os testes: python -m unittest discover __tests__"
