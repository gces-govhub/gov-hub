# Script de execução da PoC para Windows
Write-Host "=== Iniciando Execução da PoC Gov Hub ==="

# Criar diretórios necessários
Write-Host "Criando diretórios..."
New-Item -ItemType Directory -Force -Path data/raw
New-Item -ItemType Directory -Force -Path data/processed

# Download dos dados
Write-Host "Baixando dados de todas as fontes..."
python data_acquirer.py --source all

# Integração dos dados
Write-Host "Processando e integrando os dados..."
python integrate_data.py

# Verificar resultado
if (Test-Path "data/processed/integrated_poc_data.csv") {
    Write-Host " PoC executada com sucesso!"
    Write-Host "Resultados disponíveis em:"
    Write-Host "- Dados integrados: data/processed/integrated_poc_data.csv"
    Write-Host "- Relatório de resumo: data/processed/poc_summary.txt"
} else {
    Write-Host " Erro: Falha na execução da PoC"
    exit 1
}
