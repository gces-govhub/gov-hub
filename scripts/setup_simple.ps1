# setup_simple.ps1
# Script simples para instalação direta das dependências Python

Write-Host "Instalando dependências diretas sem ambiente virtual..." -ForegroundColor Cyan

# Verificar Python
$pythonVersion = python --version
Write-Host "Usando $pythonVersion" -ForegroundColor Green

# Criar requirements.txt atualizado
$requirementsContent = @"
# Core libraries - com wheels para Python 3.13/Windows
pandas==2.0.3
numpy==1.24.4
requests==2.31.0
python-dotenv==1.0.0

# Test dependencies
pytest==7.4.3
flake8==6.1.0

# Documentation
mkdocs==1.5.3
mkdocs-material==9.4.14
"@

Set-Content -Path "requirements.txt" -Value $requirementsContent -Force
Write-Host "Arquivo requirements.txt criado" -ForegroundColor Green

# Criar diretórios necessários
New-Item -ItemType Directory -Force -Path data/raw | Out-Null
New-Item -ItemType Directory -Force -Path data/processed | Out-Null
Write-Host "Diretórios criados" -ForegroundColor Green

# Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    python -m pip install pandas==2.0.3 numpy==1.24.4 requests==2.31.0
    python -m pip install -r requirements.txt
    
    # Verificar instalação
    Write-Host "Verificando instalação..." -ForegroundColor Yellow
    python -c "import pandas; import numpy; import requests; print('Instalação bem-sucedida!')"
    
    Write-Host "Dependências instaladas com sucesso!" -ForegroundColor Green
    Write-Host "Você pode executar agora: python data_acquirer.py --source all" -ForegroundColor Cyan
}
catch {
    Write-Host "Erro na instalação: $_" -ForegroundColor Red
}
