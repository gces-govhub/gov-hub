# setup_environment.ps1
# Script para configuração segura do ambiente Gov-Hub
$ErrorActionPreference = "Stop" # Parar script em caso de erro

Write-Host "Iniciando configuracao do ambiente Gov-Hub" -ForegroundColor Cyan

# Verificar Python
try {
    $pythonVersion = python --version
    Write-Host "$pythonVersion detectado" -ForegroundColor Green
}
catch {
    Write-Host "Python nao encontrado! Por favor, instale Python 3.8+ e tente novamente" -ForegroundColor Red
    exit 1
}

# Remover venv existente se presente
if (Test-Path "venv") {
    Write-Host "Removendo ambiente virtual antigo..." -ForegroundColor Yellow
    try {
        # Tentar desativar venv (silenciosamente) se estiver ativo
        try { if (Get-Command deactivate -ErrorAction SilentlyContinue) { deactivate } } catch { }
        
        # Forçar remoção do diretório
        if (Test-Path "venv") {
            Remove-Item -Recurse -Force -Path "venv" -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2  # Aguardar um pouco
            if (Test-Path "venv") {
                # Se ainda existir, tentar outro método
                cmd /c "rmdir /s /q venv" 2>$null
            }
        }
        
        if (-not (Test-Path "venv")) {
            Write-Host "Ambiente virtual antigo removido com sucesso" -ForegroundColor Green
        } else {
            Write-Host "Aviso: Não foi possível remover o diretório venv, mas tentaremos continuar" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Aviso: Não foi possível remover completamente o venv antigo: $_" -ForegroundColor Yellow
        Write-Host "Tentando continuar mesmo assim..." -ForegroundColor Yellow
    }
}

# Criar novo ambiente virtual
Write-Host "Criando novo ambiente virtual..." -ForegroundColor Cyan
try {
    # Verificar versão do Python para evitar problemas de compatibilidade
    $pythonMajorMinor = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    Write-Host "Usando Python $pythonMajorMinor para criar o ambiente virtual" -ForegroundColor Yellow
    
    python -m venv venv
    Write-Host "Ambiente virtual criado com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "Falha na criacao do ambiente virtual: $_" -ForegroundColor Red
    exit 1
}

# Ajustar política de execução temporariamente se necessário
$currentPolicy = Get-ExecutionPolicy -Scope Process
if ($currentPolicy -ne "RemoteSigned" -and $currentPolicy -ne "Unrestricted" -and $currentPolicy -ne "Bypass") {
    try {
        Write-Host "Ajustando política de execução temporariamente..." -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    } catch {
        Write-Host "Aviso: Não foi possível ajustar a política de execução: $_" -ForegroundColor Yellow
        Write-Host "Execute manualmente: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    }
}

# Ativar ambiente virtual usando método alternativo
Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan

if (Test-Path "venv\Scripts\activate.ps1") {
    try {
        # Método 1: Activar diretamente
        & "venv\Scripts\activate.ps1"
        Write-Host "Ambiente virtual ativado" -ForegroundColor Green
    }
    catch {
        try {
            # Método 2: Usar comando Import-Module
            Import-Module ".\venv\Scripts\activate.ps1"
            Write-Host "Ambiente virtual ativado via Import-Module" -ForegroundColor Green
        }
        catch {
            try {
                # Método 3: Usar cmd como fallback
                Write-Host "Tentando ativar via cmd..." -ForegroundColor Yellow
                cmd /c "venv\Scripts\activate.bat && set VIRTUAL_ENV"
                $env:VIRTUAL_ENV = (Resolve-Path "venv").Path
                $env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"
                Write-Host "Ambiente virtual ativado via cmd" -ForegroundColor Green
            }
            catch {
                Write-Host "Falha ao ativar o ambiente virtual: $_" -ForegroundColor Red
                Write-Host "Tentaremos continuar sem ativação do venv (pode causar problemas)" -ForegroundColor Yellow
            }
        }
    }
} else {
    Write-Host "ERRO: Script de ativação não encontrado em 'venv\Scripts\activate.ps1'" -ForegroundColor Red
    Write-Host "O ambiente virtual não foi criado corretamente." -ForegroundColor Red
}

# Criar/atualizar requirements.txt
try {
    Write-Host "Criando requirements.txt otimizado para Windows..." -ForegroundColor Yellow
    
    # Versões específicas que funcionam bem com Python 3.13 no Windows
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
    
    # Salvar ou atualizar requirements.txt
    Set-Content -Path "requirements.txt" -Value $requirementsContent -Force
    Write-Host "Arquivo requirements.txt criado/atualizado" -ForegroundColor Green
}
catch {
    Write-Host "Erro ao criar requirements.txt: $_" -ForegroundColor Red
}

# Atualizar pip
Write-Host "Atualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip
Write-Host "Pip atualizado" -ForegroundColor Green

# Instalar dependências
Write-Host "Instalando dependencias do projeto..." -ForegroundColor Cyan
try {
    # Instalar bibliotecas principais primeiro com --no-build-isolation para evitar compilação
    python -m pip install pandas==2.0.3 numpy==1.24.4 requests==2.31.0 --no-build-isolation
    
    # Instalar todas as dependências do requirements.txt
    python -m pip install -r requirements.txt --no-build-isolation
    
    Write-Host "Todas as dependencias instaladas com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "Erro na instalacao de dependencias: $_" -ForegroundColor Red
    
    Write-Host "Tentando método alternativo..." -ForegroundColor Yellow
    
    try {
        # Método alternativo usando pip diretamente
        & venv\Scripts\pip.exe install pandas==2.0.3 numpy==1.24.4 requests==2.31.0
        & venv\Scripts\pip.exe install -r requirements.txt
        
        Write-Host "Dependencias instaladas usando pip.exe diretamente" -ForegroundColor Green
    }
    catch {
        Write-Host "Falha no método alternativo: $_" -ForegroundColor Red
        exit 1
    }
}

# Verificar instalação
Write-Host "🔍 Verificando instalação..." -ForegroundColor Cyan
try {
    $verificationScript = @"
import sys
import pandas
import requests
import pytest
import flake8
import mkdocs

print(f"Python version: {sys.version}")
print(f"pandas version: {pandas.__version__}")
print(f"requests version: {requests.__version__}")
print(f"pytest version: {pytest.__version__}")
print("Todas as bibliotecas foram instaladas com sucesso!")
"@

    python -c $verificationScript
    Write-Host "✅ Ambiente configurado com sucesso!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Falha na verificação de bibliotecas: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 O ambiente Gov-Hub está pronto para uso!" -ForegroundColor Green
Write-Host "Execute 'python data_acquirer.py --source all' para iniciar a aquisição de dados." -ForegroundColor Cyan
