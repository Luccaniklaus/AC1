#!/bin/bash

echo "🔧 Setup da Oficina Mecânica"
echo "=============================="
echo ""

# Criar ambiente virtual
echo "1️⃣  Criando ambiente virtual..."
python -m venv .venv
echo "✅ Ambiente virtual criado"
echo ""

# Ativar ambiente (Linux/Mac)
echo "2️⃣  Ativando ambiente virtual..."
source .venv/bin/activate
echo "✅ Ambiente ativado"
echo ""

# Instalar dependências
echo "3️⃣  Instalando dependências..."
pip install -q -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# Criar banco e popular
echo "4️⃣  Criando banco de dados..."
python cadastro_sqlite.py
python dados_iniciais.py
echo "✅ Banco de dados criado e populado"
echo ""

echo "🎉 Setup concluído!"
echo ""
echo "Para iniciar a aplicação, execute:"
echo "  source .venv/bin/activate"
echo "  python app.py"
echo ""
echo "Depois acesse: http://127.0.0.1:5000"
