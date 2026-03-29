#!/bin/bash
# Script de inicialização do projeto

# Verifica se o .env existe
if [ ! -f ".env" ]; then
    echo "Arquivo .env não encontrado. Copiando .env.example..."
    cp .env.example .env
    echo "Edite o .env com suas configurações antes de continuar."
    exit 1
fi

# Instala dependências se necessário
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt --quiet

echo "Iniciando servidor..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
