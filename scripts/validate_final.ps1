# validate_final.ps1
# Script de validacao final do projeto Gov-Hub

Write-Host "=== Validacao Final do Projeto Gov-Hub ===" -ForegroundColor Cyan

$validationPassed = $true

# 1. Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Python nao encontrado" -ForegroundColor Red
    $validationPassed = $false
}

# 2. Verificar scripts essenciais
Write-Host "Verificando scripts essenciais..." -ForegroundColor Yellow
$essentialFiles = @(
    "data_acquirer_simple.py",
    "integrate_data_simple.py"
)

foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "OK: $file" -ForegroundColor Green
    } else {
        Write-Host "ERRO: $file nao encontrado" -ForegroundColor Red
        $validationPassed = $false
    }
}

# 3. Verificar estrutura de diretorios
Write-Host "Verificando estrutura de diretorios..." -ForegroundColor Yellow
$requiredDirs = @("data\raw", "data\processed")

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "OK: $dir" -ForegroundColor Green
    } else {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "CRIADO: $dir" -ForegroundColor Yellow
    }
}

# 4. Executar PoC se validacoes passaram
if ($validationPassed) {
    Write-Host "Executando PoC para validacao..." -ForegroundColor Yellow
    
    # Executar aquisicao
    python data_acquirer_simple.py --source all
    
    # Executar integracao
    python integrate_data_simple.py
    
    # Verificar resultados
    if ((Test-Path "data\processed\integrated_poc_data.csv") -and 
        (Test-Path "data\processed\poc_summary.txt")) {
        
        Write-Host "" -ForegroundColor White
        Write-Host "=== VALIDACAO CONCLUIDA COM SUCESSO ===" -ForegroundColor Green
        Write-Host "" -ForegroundColor White
        
        # Mostrar estatisticas
        $dataFile = Get-Item "data\processed\integrated_poc_data.csv"
        $summaryFile = Get-Item "data\processed\poc_summary.txt"
        
        Write-Host "Arquivos gerados:" -ForegroundColor Cyan
        Write-Host "- integrated_poc_data.csv ($($dataFile.Length) bytes)" -ForegroundColor White
        Write-Host "- poc_summary.txt ($($summaryFile.Length) bytes)" -ForegroundColor White
        
        Write-Host "" -ForegroundColor White
        Write-Host "Resumo da PoC:" -ForegroundColor Cyan
        Get-Content "data\processed\poc_summary.txt" | Select-Object -First 12 | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
        
        Write-Host "" -ForegroundColor White
        Write-Host "O projeto Gov-Hub esta funcionando corretamente!" -ForegroundColor Green
        
    } else {
        Write-Host "ERRO: Arquivos de resultado nao foram gerados" -ForegroundColor Red
        $validationPassed = $false
    }
} else {
    Write-Host "ERRO: Validacao falhou. Corrija os problemas e tente novamente." -ForegroundColor Red
}

if (-not $validationPassed) {
    exit 1
}
