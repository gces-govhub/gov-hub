# run_simple.ps1
# Script simplificado para executar a PoC sem depender de ambiente virtual

Write-Host "=== Iniciando Execução da PoC Gov Hub (Modo Simples) ===" -ForegroundColor Cyan

# Criar diretórios necessários
Write-Host "Verificando diretórios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path data/raw | Out-Null
New-Item -ItemType Directory -Force -Path data/processed | Out-Null

# Verificar dependências principais
try {
    python -c "import pandas; import requests" 2>$null
    Write-Host "Dependências verificadas com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Dependências não instaladas. Execute setup_simple.ps1 primeiro." -ForegroundColor Red
    exit 1
}

# Download dos dados
Write-Host "Baixando dados de todas as fontes..." -ForegroundColor Yellow
python data_acquirer.py --source all

# Integração dos dados
Write-Host "Processando e integrando os dados..." -ForegroundColor Yellow
python integrate_data.py

# Verificar resultado
if (Test-Path "data/processed/integrated_poc_data.csv") {
    Write-Host "✓ PoC executada com sucesso!" -ForegroundColor Green
    Write-Host "Resultados disponíveis em:" -ForegroundColor Cyan
    Write-Host "- Dados integrados: data/processed/integrated_poc_data.csv" -ForegroundColor White
    Write-Host "- Relatório de resumo: data/processed/poc_summary.txt" -ForegroundColor White
    
    # Exibir resumo
    Write-Host "`nResumo da integração:" -ForegroundColor Cyan
    if (Test-Path "data/processed/poc_summary.txt") {
        Get-Content "data/processed/poc_summary.txt" | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "X Erro: Falha na execução da PoC" -ForegroundColor Red
    exit 1
}
