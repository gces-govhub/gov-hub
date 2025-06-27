# run_final.ps1
# Script final para execucao da PoC Gov-Hub - Fase 2
# Versao atualizada para aquisicao real de dados governamentais

Write-Host "=== Gov-Hub Fase 2 - Execucao com Dados Reais ===" -ForegroundColor Cyan
Write-Host "Data/Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

# Verificar se arquivos essenciais existem
$essentialFiles = @("data_acquirer.py", "integrate_data_simple.py", "config.json")
foreach ($file in $essentialFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "ERRO: Arquivo essencial nao encontrado: $file" -ForegroundColor Red
        exit 1
    }
}

# Verificar se diretorios existem e criar se necessario
Write-Host "Preparando estrutura de diretorios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\raw" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null
New-Item -ItemType Directory -Force -Path "data\temp" | Out-Null

# Executar aquisicao de dados REAIS
Write-Host "" -ForegroundColor White
Write-Host "=== FASE 1: AQUISICAO DE DADOS REAIS ===" -ForegroundColor Green
Write-Host "Tentando baixar dados das fontes oficiais:" -ForegroundColor Yellow
Write-Host "  * SIAFI (Portal da Transparencia)" -ForegroundColor Gray
Write-Host "  * Compras.gov.br" -ForegroundColor Gray  
Write-Host "  * TransfereGov" -ForegroundColor Gray
Write-Host ""

# Usar o novo data_acquirer.py com dados reais
python data_acquirer.py --source all --verbose

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO na aquisicao de dados reais" -ForegroundColor Red
    Write-Host "Verificando se dados de amostra foram gerados..." -ForegroundColor Yellow
    
    # Verificar se pelo menos dados de amostra existem
    $csvFiles = Get-ChildItem "data\raw\*.csv" -ErrorAction SilentlyContinue
    if ($csvFiles.Count -eq 0) {
        Write-Host "ERRO CRITICO: Nenhum dado disponivel (nem real nem amostra)" -ForegroundColor Red
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
Write-Host "Processando e integrando dados adquiridos..." -ForegroundColor Yellow
python integrate_data_simple.py

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
    Write-Host "=== GOV-HUB FASE 2 EXECUTADA COM SUCESSO ===" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    
    # Determinar se usou dados reais ou amostra
    $realDataIndicators = @("siafi_202", "contratos_202", "convenios_202")
    $sampleDataIndicators = @("amostra", "sample")
    
    $csvFiles = Get-ChildItem "data\raw\*.csv" -ErrorAction SilentlyContinue
    $hasRealData = $false
    $hasSampleData = $false
    
    foreach ($file in $csvFiles) {
        $fileName = $file.Name.ToLower()
        if ($realDataIndicators | Where-Object { $fileName.Contains($_) }) {
            $hasRealData = $true
        }
        if ($sampleDataIndicators | Where-Object { $fileName.Contains($_) }) {
            $hasSampleData = $true
        }
    }
    
    if ($hasRealData -and -not $hasSampleData) {
        Write-Host "DADOS REAIS: Pipeline funcionando com dados oficiais!" -ForegroundColor Magenta
    } elseif ($hasRealData -and $hasSampleData) {
        Write-Host "DADOS MISTOS: Combinacao de dados reais e amostra" -ForegroundColor Yellow
    } else {
        Write-Host "DADOS DE AMOSTRA: Funcionando com fallback (fontes indisponiveis)" -ForegroundColor Cyan
    }
    
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
    Write-Host "Dados brutos:" -ForegroundColor White
    $csvFiles = Get-ChildItem "data\raw\*.csv" -ErrorAction SilentlyContinue
    foreach ($file in $csvFiles) {
        Write-Host "  [ARQUIVO] data\raw\$($file.Name)" -ForegroundColor Gray
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "Logs:" -ForegroundColor White
    if (Test-Path "govhub_data_acquisition.log") {
        Write-Host "  [ARQUIVO] govhub_data_acquisition.log" -ForegroundColor Gray
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "PROXIMOS PASSOS SUGERIDOS:" -ForegroundColor Cyan
    Write-Host "  1. Analisar os dados em integrated_poc_data.csv" -ForegroundColor White
    Write-Host "  2. Verificar logs para detalhes da aquisicao" -ForegroundColor White
    Write-Host "  3. Implementar dashboards e visualizacoes" -ForegroundColor White
    Write-Host "  4. Configurar execucao automatica (cron/task scheduler)" -ForegroundColor White
    
} else {
    Write-Host "=== EXECUCAO FALHOU ===" -ForegroundColor Red
    Write-Host "" -ForegroundColor White
    Write-Host "Verifique os logs para diagnostico:" -ForegroundColor Yellow
    if (Test-Path "govhub_data_acquisition.log") {
        Write-Host "  [ARQUIVO] govhub_data_acquisition.log" -ForegroundColor Gray
    }
    exit 1
}
