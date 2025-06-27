# run_final.ps1
# Script final para execucao da PoC Gov-Hub - Estrutura Modular
# Versao refatorada para nova arquitetura

# Guardar diretório atual e voltar para o diretório raiz do projeto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "=== Gov-Hub Pipeline - Estrutura Modular ===" -ForegroundColor Cyan
Write-Host "Data/Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

# Verificar se módulos essenciais existem
$essentialModules = @(
    "src\govhub\core\acquisition.py", 
    "src\govhub\core\integration.py", 
    "config/config.json"
)

foreach ($module in $essentialModules) {
    if (-not (Test-Path $module)) {
        Write-Host "ERRO: Modulo essencial nao encontrado: $module" -ForegroundColor Red
        exit 1
    }
}

# Verificar se diretorios existem e criar se necessario
Write-Host "Preparando estrutura de diretorios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\raw" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null
New-Item -ItemType Directory -Force -Path "data\temp" | Out-Null

# Executar validação do sistema
Write-Host "" -ForegroundColor White
Write-Host "=== FASE 0: VALIDACAO DO SISTEMA ===" -ForegroundColor Blue
Write-Host "Validando estrutura modular..." -ForegroundColor Yellow

try {
    python -m src.govhub.utils.validation
    if ($LASTEXITCODE -ne 0) {
        Write-Host "AVISO: Validacao encontrou problemas, mas continuando..." -ForegroundColor Yellow
    } else {
        Write-Host "Sistema validado com sucesso" -ForegroundColor Green
    }
}
catch {
    Write-Host "AVISO: Erro na validacao, mas continuando: $_" -ForegroundColor Yellow
}

# Executar aquisicao de dados
Write-Host "" -ForegroundColor White
Write-Host "=== FASE 1: AQUISICAO DE DADOS ===" -ForegroundColor Green
Write-Host "Executando modulo de aquisicao..." -ForegroundColor Yellow
Write-Host "  * Usando: src.govhub.core.acquisition" -ForegroundColor Gray
Write-Host ""

# Usar o novo módulo de aquisição
python -m src.govhub.core.acquisition --source all

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO na aquisicao de dados" -ForegroundColor Red
    Write-Host "Verificando se dados de amostra foram gerados..." -ForegroundColor Yellow
    
    # Verificar se pelo menos dados de amostra existem
    $csvFiles = Get-ChildItem "data\raw\*.csv" -ErrorAction SilentlyContinue
    if ($csvFiles.Count -eq 0) {
        Write-Host "ERRO CRITICO: Nenhum dado disponivel" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "Continuando com dados de amostra disponiveis" -ForegroundColor Yellow
    }
}

# Verificar dados baixados
Write-Host "" -ForegroundColor White
Write-Host "=== VERIFICACAO DOS DADOS ADQUIRIDOS ===" -ForegroundColor Green
$csvFiles = Get-ChildItem "data\raw\*.csv" -ErrorAction SilentlyContinue
if ($csvFiles.Count -gt 0) {
    Write-Host "Arquivos de dados encontrados:" -ForegroundColor Green
    foreach ($file in $csvFiles) {
        $sizeKB = [math]::Round($file.Length / 1024, 1)
        Write-Host "  [ARQUIVO] $($file.Name) ($sizeKB KB)" -ForegroundColor Gray
    }
} else {
    Write-Host "AVISO: Nenhum arquivo CSV encontrado" -ForegroundColor Yellow
}

# Executar integracao de dados
Write-Host "" -ForegroundColor White
Write-Host "=== FASE 2: INTEGRACAO DE DADOS ===" -ForegroundColor Green
Write-Host "Executando modulo de integracao..." -ForegroundColor Yellow
Write-Host "  * Usando: src.govhub.core.integration" -ForegroundColor Gray

python -m src.govhub.core.integration

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO na integracao de dados" -ForegroundColor Red
    exit 1
}

# Verificar resultados finais
Write-Host "" -ForegroundColor White
Write-Host "=== FASE 3: VERIFICACAO DOS RESULTADOS ===" -ForegroundColor Green

$resultadosOk = $true

# Verificar arquivo de dados integrados
if (Test-Path "data\processed\integrated_poc_data.csv") {
    $fileSize = (Get-Item "data\processed\integrated_poc_data.csv").Length
    $fileSizeKB = [math]::Round($fileSize / 1024, 1)
    Write-Host "SUCESSO: Arquivo de dados integrados criado ($fileSizeKB KB)" -ForegroundColor Green
    
    # Verificar se tem conteudo
    $lineCount = (Get-Content "data\processed\integrated_poc_data.csv" | Measure-Object -Line).Lines
    Write-Host "   [DADOS] $lineCount linhas de dados" -ForegroundColor Gray
} else {
    Write-Host "ERRO: Arquivo de dados integrados nao encontrado" -ForegroundColor Red
    $resultadosOk = $false
}

# Verificar relatorio de resumo
if (Test-Path "data\processed\poc_summary.txt") {
    Write-Host "SUCESSO: Relatorio de resumo criado" -ForegroundColor Green
} else {
    Write-Host "ERRO: Relatorio de resumo nao encontrado" -ForegroundColor Red
    $resultadosOk = $false
}

# Verificar logs de aquisicao
if (Test-Path "govhub_data_acquisition.log") {
    $logSize = (Get-Item "govhub_data_acquisition.log").Length
    if ($logSize -gt 0) {
        Write-Host "SUCESSO: Log de aquisicao gerado (detalhes disponiveis)" -ForegroundColor Green
    }
}

# Resultado final
Write-Host "" -ForegroundColor White
if ($resultadosOk) {
    Write-Host "=== GOV-HUB PIPELINE EXECUTADO COM SUCESSO ===" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    Write-Host "ESTRUTURA MODULAR: Pipeline funcionando com nova arquitetura!" -ForegroundColor Magenta
    Write-Host "" -ForegroundColor White
    
    # Mostrar resumo detalhado
    Write-Host "=== RESUMO DA EXECUCAO ===" -ForegroundColor Cyan
    if (Test-Path "data\processed\poc_summary.txt") {
        Get-Content "data\processed\poc_summary.txt" | Select-Object -First 20 | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "=== ARQUIVOS GERADOS ===" -ForegroundColor Cyan
    Write-Host "Dados principais:" -ForegroundColor White
    Write-Host "  [ARQUIVO] data\processed\integrated_poc_data.csv" -ForegroundColor White
    Write-Host "  [ARQUIVO] data\processed\poc_summary.txt" -ForegroundColor White
    
    Write-Host "" -ForegroundColor White
    Write-Host "Modulos utilizados:" -ForegroundColor White
    Write-Host "  [MODULO] src\govhub\core\acquisition.py" -ForegroundColor Gray
    Write-Host "  [MODULO] src\govhub\core\integration.py" -ForegroundColor Gray
    Write-Host "  [MODULO] src\govhub\utils\validation.py" -ForegroundColor Gray
    
    Write-Host "" -ForegroundColor White
    Write-Host "Dados brutos:" -ForegroundColor White
    $csvFiles = Get-ChildItem "data\raw\*.csv" -ErrorAction SilentlyContinue
    foreach ($file in $csvFiles) {
        Write-Host "  [ARQUIVO] data\raw\$($file.Name)" -ForegroundColor Gray
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "PROXIMOS PASSOS SUGERIDOS:" -ForegroundColor Cyan
    Write-Host "  1. Implementar dashboards e visualizacoes" -ForegroundColor White
    Write-Host "  2. Adicionar testes unitários em tests/" -ForegroundColor White
    Write-Host "  3. Criar notebooks de análise em notebooks/" -ForegroundColor White
    Write-Host "  4. Configurar CI/CD para execucao automatica" -ForegroundColor White
    
} else {
    Write-Host "=== EXECUCAO FALHOU ===" -ForegroundColor Red
    Write-Host "" -ForegroundColor White
    Write-Host "Verifique os logs para diagnostico:" -ForegroundColor Yellow
    if (Test-Path "govhub_data_acquisition.log") {
        Write-Host "  [ARQUIVO] govhub_data_acquisition.log" -ForegroundColor Gray
    }
    exit 1
}
