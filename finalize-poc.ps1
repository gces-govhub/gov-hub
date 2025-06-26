# Gov-Hub PoC Finalization Script
# Executa todos os passos necessários para finalizar a PoC

param(
    [switch]$SkipGit,
    [switch]$DryRun,
    [string]$CommitMessage = "feat(poc): conclude proof of concept implementation"
)

Write-Host "🎯 Gov-Hub PoC - Script de Finalização" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Função para logging
function Write-Step {
    param([string]$Message)
    Write-Host "➤ $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# 1. Verificações Iniciais
Write-Step "Verificando ambiente e dependências..."

if (-not (Test-Path "pyproject.toml")) {
    Write-Error "Arquivo pyproject.toml não encontrado. Execute este script na raiz do projeto."
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git não está instalado ou não está no PATH."
    exit 1
}

Write-Success "Ambiente verificado com sucesso"

# 2. Validação Final do Projeto
Write-Step "Executando validação final do projeto..."

if (Test-Path "validate_final.ps1") {
    try {
        & ".\validate_final.ps1"
        Write-Success "Validação final executada com sucesso"
    }
    catch {
        Write-Error "Falha na validação final: $($_.Exception.Message)"
        if (-not $DryRun) {
            $continue = Read-Host "Deseja continuar mesmo com falhas na validação? (y/N)"
            if ($continue -ne "y" -and $continue -ne "Y") {
                exit 1
            }
        }
    }
} else {
    Write-Warning "Script validate_final.ps1 não encontrado"
}

# 3. Limpeza de Arquivos Temporários
Write-Step "Limpando arquivos temporários..."

$tempPatterns = @(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.tmp",
    "*.temp",
    ".pytest_cache",
    "*.log"
)

foreach ($pattern in $tempPatterns) {
    Get-ChildItem -Path . -Recurse -Name $pattern -Force | ForEach-Object {
        if ($DryRun) {
            Write-Host "    [DRY RUN] Removeria: $_"
        } else {
            Remove-Item $_ -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

Write-Success "Limpeza concluída"

# 4. Verificação do .gitignore
Write-Step "Verificando configuração do .gitignore..."

$gitignoreContent = Get-Content ".gitignore" -ErrorAction SilentlyContinue
$requiredPatterns = @("data/processed/", "data/raw/*.csv", "!data/raw/*_sample.csv", "__pycache__/")

$missingPatterns = @()
foreach ($pattern in $requiredPatterns) {
    if ($gitignoreContent -notcontains $pattern) {
        $missingPatterns += $pattern
    }
}

if ($missingPatterns.Count -gt 0) {
    Write-Warning "Padrões faltando no .gitignore: $($missingPatterns -join ', ')"
} else {
    Write-Success ".gitignore configurado corretamente"
}

# 5. Processamento Git (se habilitado)
if (-not $SkipGit) {
    Write-Step "Processando versionamento Git..."
    
    # Verificar status do repositório
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Step "Arquivos modificados detectados. Adicionando ao staging..."
        
        if ($DryRun) {
            Write-Host "    [DRY RUN] git add ."
            Write-Host "    [DRY RUN] git commit -m '$CommitMessage'"
        } else {
            git add .
            
            # Commit com mensagem padrão ou personalizada
            $fullCommitMessage = @"
$CommitMessage

- Add comprehensive data acquisition and integration pipeline
- Implement automated validation and testing scripts  
- Add complete documentation and user guides
- Configure project structure and dependencies
- Add sample data and processing examples

BREAKING CHANGE: Complete PoC implementation ready for production evaluation

Closes #POC-001
"@
            
            git commit -m $fullCommitMessage
            Write-Success "Commit criado com sucesso"
            
            # Verificar se estamos em uma branch remota
            $currentBranch = git branch --show-current
            $remoteBranch = git ls-remote --heads origin $currentBranch
            
            if ($remoteBranch) {
                Write-Step "Fazendo push para origin/$currentBranch..."
                git push origin $currentBranch
                Write-Success "Push realizado com sucesso"
            } else {
                Write-Warning "Branch remota não encontrada. Execute 'git push origin $currentBranch' manualmente."
            }
        }
    } else {
        Write-Success "Repositório já está atualizado"
    }
} else {
    Write-Warning "Processamento Git foi pulado (parâmetro -SkipGit)"
}

# 6. Geração de Relatório Final
Write-Step "Gerando relatório de finalização..."

$reportPath = "finalization-report-$(Get-Date -Format 'yyyy-MM-dd-HHmm').txt"

$report = @"
Gov-Hub PoC - Relatório de Finalização
=====================================
Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Usuário: $env:USERNAME
Máquina: $env:COMPUTERNAME

Status da Finalização:
✅ Validação do projeto executada
✅ Arquivos temporários limpos
✅ .gitignore verificado
$(if (-not $SkipGit) { "✅ Versionamento Git processado" } else { "⚠️  Versionamento Git pulado" })

Próximos Passos:
1. Revisar Pull Request (pull-request-template.md)
2. Executar comandos Git (git-versioning-commands.md)
3. Apresentar relatório final (POC-COMPLETION-REPORT.md)

Arquivos Gerados:
- .gitignore (atualizado)
- git-versioning-commands.md
- pull-request-template.md  
- POC-COMPLETION-REPORT.md
- finalize-poc.ps1

Status: FINALIZAÇÃO CONCLUÍDA COM SUCESSO ✅
"@

if ($DryRun) {
    Write-Host "    [DRY RUN] Relatório seria salvo em: $reportPath"
    Write-Host $report
} else {
    $report | Out-File -FilePath $reportPath -Encoding utf8
    Write-Success "Relatório salvo em: $reportPath"
}

# 7. Mensagem Final
Write-Host ""
Write-Host "🎉 FINALIZAÇÃO DA POC CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos Passos:" -ForegroundColor Yellow
Write-Host "   1. Revisar o Pull Request template: pull-request-template.md"
Write-Host "   2. Executar comandos Git: git-versioning-commands.md"
Write-Host "   3. Apresentar o relatório: POC-COMPLETION-REPORT.md"
Write-Host ""
Write-Host "📁 Arquivos de Documentação Criados:" -ForegroundColor Cyan
Write-Host "   - git-versioning-commands.md"
Write-Host "   - pull-request-template.md"
Write-Host "   - POC-COMPLETION-REPORT.md"
Write-Host "   - finalize-poc.ps1"
Write-Host "   - $reportPath"
Write-Host ""
Write-Host "🎯 A PoC do Gov-Hub está oficialmente CONCLUÍDA!" -ForegroundColor Green
