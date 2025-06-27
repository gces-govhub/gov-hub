# validate_simple.ps1
# Validação simplificada sem dependência de ambiente virtual

Write-Host "=== Validação Simplificada do Projeto Gov-Hub ===" -ForegroundColor Cyan

# 1. Verificar Python e dependências
Write-Host "Verificando ambiente Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
    
    # Verificar dependências principais
    python -c "import pandas; import requests; print('Dependências principais OK')"
    $depsOk = $true
}
catch {
    Write-Host "Erro na verificação de dependências: $_" -ForegroundColor Red
    Write-Host "Execute setup_simple.ps1 primeiro!" -ForegroundColor Yellow
    $depsOk = $false
}

if (-not $depsOk) {
    exit 1
}

# 2. Verificar arquivos essenciais
Write-Host "`nVerificando arquivos do projeto..." -ForegroundColor Yellow
$essentialFiles = @(
    "data_acquirer.py",
    "integrate_data.py",
    "requirements.txt"
)

$allFilesExist = $true
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    }
    else {
        Write-Host "X $file não encontrado!" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "Arquivos essenciais ausentes!" -ForegroundColor Red
    exit 1
}

# 3. Verificar diretórios de dados
Write-Host "`nVerificando diretórios de dados..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path data/raw | Out-Null
New-Item -ItemType Directory -Force -Path data/processed | Out-Null
Write-Host "Diretórios OK" -ForegroundColor Green

# 4. Executar a PoC
Write-Host "`nExecutando a PoC..." -ForegroundColor Yellow
python data_acquirer.py --source all
python integrate_data.py

# 5. Verificar resultados
Write-Host "`nVerificando resultados..." -ForegroundColor Yellow
if (Test-Path "data/processed/integrated_poc_data.csv" -and 
    Test-Path "data/processed/poc_summary.txt") {
    Write-Host "✓ Arquivos de resultados encontrados" -ForegroundColor Green
    
    # Mostrar estatísticas
    $fileSize = (Get-Item "data/processed/integrated_poc_data.csv").Length / 1KB
    Write-Host "Tamanho do arquivo de dados: $([Math]::Round($fileSize, 2)) KB" -ForegroundColor Cyan
    
    # Mostrar resumo
    Write-Host "`nResumo da PoC:" -ForegroundColor Cyan
    Get-Content "data/processed/poc_summary.txt" | Select-Object -First 10 | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
    
    Write-Host "`n✓ VALIDAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
}
else {
    Write-Host "X Arquivos de resultado não encontrados!" -ForegroundColor Red
    exit 1
}
