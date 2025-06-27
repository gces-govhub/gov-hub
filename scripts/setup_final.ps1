# setup_final.ps1
# Script final e robusto para configuracao do ambiente Gov-Hub
# Atualizado para a nova estrutura modular

# Guardar diretório atual e voltar para o diretório raiz do projeto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "=== Setup Final do Projeto Gov-Hub ===" -ForegroundColor Cyan

# Verificar Python
$pythonVersion = python --version
Write-Host "Python detectado: $pythonVersion" -ForegroundColor Green

# Criar estrutura de diretorios necessarios
Write-Host "Criando estrutura de diretorios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\raw" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null
New-Item -ItemType Directory -Force -Path "src\govhub\core" | Out-Null
New-Item -ItemType Directory -Force -Path "src\govhub\utils" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "tests" | Out-Null
New-Item -ItemType Directory -Force -Path "notebooks" | Out-Null

Write-Host "Diretorios criados com sucesso" -ForegroundColor Green

# Verificar se os módulos principais existem
$modulesOk = $true

if (-not (Test-Path "src\govhub\core\acquisition.py")) {
    Write-Host "ERRO: src\govhub\core\acquisition.py nao encontrado!" -ForegroundColor Red
    $modulesOk = $false
}

if (-not (Test-Path "src\govhub\core\integration.py")) {
    Write-Host "ERRO: src\govhub\core\integration.py nao encontrado!" -ForegroundColor Red
    $modulesOk = $false
}

if (-not (Test-Path "src\govhub\utils\validation.py")) {
    Write-Host "ERRO: src\govhub\utils\validation.py nao encontrado!" -ForegroundColor Red
    $modulesOk = $false
}

if ($modulesOk) {
    Write-Host "Modulos principais encontrados" -ForegroundColor Green
} else {
    Write-Host "Modulos principais ausentes. Verifique a instalacao." -ForegroundColor Red
    exit 1
}

# Testar sintaxe dos módulos Python
Write-Host "Testando sintaxe dos modulos..." -ForegroundColor Yellow

try {
    # Testar compilação dos módulos principais
    python -m py_compile src\govhub\core\acquisition.py
    python -m py_compile src\govhub\core\integration.py
    python -m py_compile src\govhub\utils\validation.py
    Write-Host "Modulos compilados com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "ERRO na compilacao dos modulos: $_" -ForegroundColor Red
    exit 1
}

# Executar validação do sistema
Write-Host "Executando validacao do sistema..." -ForegroundColor Yellow
try {
    python -m src.govhub.utils.validation
    Write-Host "Validacao do sistema concluida" -ForegroundColor Green
}
catch {
    Write-Host "AVISO: Validacao encontrou problemas: $_" -ForegroundColor Yellow
    Write-Host "Continuando com a configuracao..." -ForegroundColor Yellow
}

Write-Host "" -ForegroundColor White
Write-Host "=== CONFIGURACAO CONCLUIDA ===" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "1. Execute: .\scripts\run_final.ps1" -ForegroundColor White
Write-Host "2. Verifique os resultados em data\processed" -ForegroundColor White
Write-Host "3. Para validacao: python -m src.govhub.utils.validation" -ForegroundColor White
