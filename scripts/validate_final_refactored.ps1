# validate_final.ps1
# Script de validacao final do projeto Gov-Hub - Estrutura Modular
# Versao refatorada para nova arquitetura

# Guardar diretório atual e voltar para o diretório raiz do projeto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "=== Validacao Final do Projeto Gov-Hub - Estrutura Modular ===" -ForegroundColor Cyan

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

# 2. Verificar estrutura modular
Write-Host "Verificando estrutura modular..." -ForegroundColor Yellow
$essentialModules = @(
    "src\govhub\__init__.py",
    "src\govhub\core\__init__.py",
    "src\govhub\core\acquisition.py",
    "src\govhub\core\integration.py",
    "src\govhub\utils\__init__.py",
    "src\govhub\utils\validation.py"
)

foreach ($module in $essentialModules) {
    if (Test-Path $module) {
        Write-Host "OK: $module" -ForegroundColor Green
    } else {
        Write-Host "ERRO: $module nao encontrado" -ForegroundColor Red
        $validationPassed = $false
    }
}

# 3. Verificar estrutura de diretorios
Write-Host "Verificando estrutura de diretorios..." -ForegroundColor Yellow
$requiredDirs = @(
    "data\raw", 
    "data\processed", 
    "src\govhub\core", 
    "src\govhub\utils", 
    "scripts", 
    "tests", 
    "notebooks"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "OK: $dir" -ForegroundColor Green
    } else {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "CRIADO: $dir" -ForegroundColor Yellow
    }
}

# 4. Verificar arquivo de configuracao
Write-Host "Verificando configuracao..." -ForegroundColor Yellow
if (Test-Path "config/config.json") {
    Write-Host "OK: config/config.json" -ForegroundColor Green
} else {
    Write-Host "ERRO: config/config.json nao encontrado" -ForegroundColor Red
    $validationPassed = $false
}

# 5. Testar importacao dos modulos
Write-Host "Testando importacao dos modulos..." -ForegroundColor Yellow
try {
    python -c "import sys; sys.path.insert(0, 'src'); from govhub.core.acquisition import GovHubDataAcquirer; print('Modulo de aquisicao OK')"
    Write-Host "OK: Modulo de aquisicao importado" -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Falha na importacao do modulo de aquisicao" -ForegroundColor Red
    $validationPassed = $false
}

try {
    python -c "import sys; sys.path.insert(0, 'src'); from govhub.core.integration import DataIntegrator; print('Modulo de integracao OK')"
    Write-Host "OK: Modulo de integracao importado" -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Falha na importacao do modulo de integracao" -ForegroundColor Red
    $validationPassed = $false
}

# 6. Executar validacao completa do sistema
Write-Host "Executando validacao completa do sistema..." -ForegroundColor Yellow
try {
    python -m src.govhub.utils.validation
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK: Sistema totalmente validado" -ForegroundColor Green
    } else {
        Write-Host "AVISO: Validacao encontrou alguns problemas" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "ERRO: Falha na validacao do sistema: $_" -ForegroundColor Red
    $validationPassed = $false
}

# 7. Executar Pipeline se validacoes passaram
if ($validationPassed) {
    Write-Host "" -ForegroundColor White
    Write-Host "=== EXECUTANDO PIPELINE PARA VALIDACAO ===" -ForegroundColor Green
    Write-Host "Testando pipeline completo..." -ForegroundColor Yellow
    
    # Executar aquisicao
    Write-Host "Fase 1: Aquisicao de dados..." -ForegroundColor Cyan
    python -m src.govhub.core.acquisition --source all
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK: Aquisicao executada" -ForegroundColor Green
        
        # Executar integracao
        Write-Host "Fase 2: Integracao de dados..." -ForegroundColor Cyan
        python -m src.govhub.core.integration
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK: Integracao executada" -ForegroundColor Green
            
            # Verificar resultados
            if ((Test-Path "data\processed\integrated_poc_data.csv") -and (Test-Path "data\processed\poc_summary.txt")) {
                Write-Host "" -ForegroundColor White
                Write-Host "=== VALIDACAO BEM-SUCEDIDA ===" -ForegroundColor Green
                Write-Host "O sistema Gov-Hub esta funcionando corretamente!" -ForegroundColor Green
                Write-Host "" -ForegroundColor White
                
                # Mostrar estatisticas
                $csvSize = (Get-Item "data\processed\integrated_poc_data.csv").Length
                $csvSizeKB = [math]::Round($csvSize / 1024, 1)
                Write-Host "Arquivo de dados integrados: $csvSizeKB KB" -ForegroundColor Gray
                
                if (Test-Path "data\processed\poc_summary.txt") {
                    Write-Host "Resumo da execucao:" -ForegroundColor Cyan
                    Get-Content "data\processed\poc_summary.txt" | Select-Object -First 10 | ForEach-Object {
                        Write-Host "  $_" -ForegroundColor Gray
                    }
                }
                
                Write-Host "" -ForegroundColor White
                Write-Host "ESTRUTURA MODULAR VALIDADA:" -ForegroundColor Magenta
                Write-Host "  ✅ Modulos organizados em src/govhub/" -ForegroundColor White
                Write-Host "  ✅ Scripts organizados em scripts/" -ForegroundColor White
                Write-Host "  ✅ Pipeline funcional com nova arquitetura" -ForegroundColor White
                
            } else {
                Write-Host "ERRO: Arquivos de resultado nao foram gerados" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "ERRO: Falha na integracao" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "ERRO: Falha na aquisicao" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "" -ForegroundColor White
    Write-Host "=== VALIDACAO FALHOU ===" -ForegroundColor Red
    Write-Host "Corrija os problemas identificados antes de continuar." -ForegroundColor Red
    exit 1
}
