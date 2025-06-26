# setup_final.ps1
# Script final e robusto para configuracao do ambiente Gov-Hub

Write-Host "=== Setup Final do Projeto Gov-Hub ===" -ForegroundColor Cyan

# Verificar Python
$pythonVersion = python --version
Write-Host "Python detectado: $pythonVersion" -ForegroundColor Green

# Criar diretorios necessarios
Write-Host "Criando estrutura de diretorios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\raw" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null
New-Item -ItemType Directory -Force -Path ".github\workflows" | Out-Null
New-Item -ItemType Directory -Force -Path "docs" | Out-Null

Write-Host "Diretorios criados com sucesso" -ForegroundColor Green

# Verificar se os scripts simplificados existem
$scriptsOk = $true

if (-not (Test-Path "data_acquirer_simple.py")) {
    Write-Host "ERRO: data_acquirer_simple.py nao encontrado!" -ForegroundColor Red
    $scriptsOk = $false
}

if (-not (Test-Path "integrate_data_simple.py")) {
    Write-Host "ERRO: integrate_data_simple.py nao encontrado!" -ForegroundColor Red
    $scriptsOk = $false
}

if ($scriptsOk) {
    Write-Host "Scripts essenciais encontrados" -ForegroundColor Green
} else {
    Write-Host "Scripts essenciais ausentes. Verifique a instalacao." -ForegroundColor Red
    exit 1
}

# Testar execucao dos scripts
Write-Host "Testando execucao dos scripts..." -ForegroundColor Yellow

try {
    # Testar syntax dos scripts Python
    python -m py_compile data_acquirer_simple.py
    python -m py_compile integrate_data_simple.py
    Write-Host "Scripts compilados com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "ERRO na compilacao dos scripts: $_" -ForegroundColor Red
    exit 1
}

Write-Host "" -ForegroundColor White
Write-Host "=== CONFIGURACAO CONCLUIDA ===" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "1. Execute: .\run_final.ps1" -ForegroundColor White
Write-Host "2. Verifique os resultados em data\processed" -ForegroundColor White
