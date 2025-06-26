#!/bin/bash
set -e  # Exit on error

echo "=== Iniciando Execução da PoC Gov Hub ==="

# Criar diretórios necessários
echo "Criando diretórios..."
mkdir -p data/raw data/processed

# Download dos dados
echo "Baixando dados de todas as fontes..."
python data_acquirer.py --source all

# Integração dos dados
echo "Processando e integrando os dados..."
python integrate_data.py

# Verificar resultado
if [ -f "data/processed/integrated_poc_data.csv" ]; then
    echo "✅ PoC executada com sucesso!"
    echo "Resultados disponíveis em:"
    echo "- Dados integrados: data/processed/integrated_poc_data.csv"
    echo "- Relatório de resumo: data/processed/poc_summary.txt"
else
    echo "❌ Erro: Falha na execução da PoC"
    exit 1
fi
