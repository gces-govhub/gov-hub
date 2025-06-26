# run_final.ps1
# Script final para execucao da PoC Gov-Hub

Write-Host "=== Execucao Final da PoC Gov-Hub ===" -ForegroundColor Cyan

# Verificar se diretorios existem
New-Item -ItemType Directory -Force -Path "data\raw" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null

# Executar aquisicao de dados
Write-Host "Executando aquisicao de dados..." -ForegroundColor Yellow
python data_acquirer_simple.py --source all

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO na aquisicao de dados" -ForegroundColor Red
    exit 1
}

# Executar integracao de dados
Write-Host "Executando integracao de dados..." -ForegroundColor Yellow
python integrate_data_simple.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO na integracao de dados" -ForegroundColor Red
    exit 1
}

# Verificar resultados
Write-Host "Verificando resultados..." -ForegroundColor Yellow

$resultadosOk = $true

if (Test-Path "data\processed\integrated_poc_data.csv") {
    $fileSize = (Get-Item "data\processed\integrated_poc_data.csv").Length
    Write-Host "Arquivo de dados integrados criado ($fileSize bytes)" -ForegroundColor Green
} else {
    Write-Host "ERRO: Arquivo de dados integrados nao encontrado" -ForegroundColor Red
    $resultadosOk = $false
}

if (Test-Path "data\processed\poc_summary.txt") {
    Write-Host "Relatorio de resumo criado" -ForegroundColor Green
} else {
    Write-Host "ERRO: Relatorio de resumo nao encontrado" -ForegroundColor Red
    $resultadosOk = $false
}

if ($resultadosOk) {
    Write-Host "" -ForegroundColor White
    Write-Host "=== POC EXECUTADA COM SUCESSO ===" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    
    # Mostrar resumo
    Write-Host "Resumo da execucao:" -ForegroundColor Cyan
    if (Test-Path "data\processed\poc_summary.txt") {
        Get-Content "data\processed\poc_summary.txt" | Select-Object -First 15 | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "Arquivos gerados:" -ForegroundColor Cyan
    Write-Host "- data\processed\integrated_poc_data.csv" -ForegroundColor White
    Write-Host "- data\processed\poc_summary.txt" -ForegroundColor White
} else {
    Write-Host "ERRO: PoC nao foi concluida corretamente" -ForegroundColor Red
    exit 1
}
