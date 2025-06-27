# Gov-Hub Fase 2 - Guia de Aquisição Real de Dados

## Visão Geral

A Fase 2 do Gov-Hub marca a evolução da Prova de Conceito (PoC) para um protótipo funcional que realiza aquisição **real** de dados dos portais governamentais brasileiros.

### Principais Melhorias

1. **Aquisição Real de Dados**: Substituição completa dos dados de amostra por downloads reais
2. **Configuração Externa**: Sistema de configuração flexível via `config.json`
3. **Resiliência a Falhas**: Tratamento robusto de erros com fallback automático
4. **Logging Avançado**: Sistema detalhado de logs para diagnóstico
5. **Suporte Multi-formato**: ZIP, CSV, JSON com descompactação automática
6. **Rate Limiting**: Controle de requisições para evitar bloqueios

## Arquitetura do Sistema

```
Gov-Hub Fase 2
├── config.json              # Configurações das fontes de dados
├── data_acquirer.py          # Motor principal de aquisição
├── integrate_data_simple.py  # Processamento e integração
├── run_final.ps1            # Orquestração completa
└── data/
    ├── raw/                 # Dados brutos baixados
    ├── processed/           # Dados integrados
    └── temp/                # Arquivos temporários
```

## Fontes de Dados Configuradas

### 1. SIAFI (Sistema Integrado de Administração Financeira)
- **Portal da Transparência**: Despesas de execução orçamentária
- **Tesouro Transparente**: Dados de execução orçamentária
- **Formato**: ZIP/CSV
- **Fallback**: Dados de amostra com estrutura realista

### 2. Compras.gov.br
- **API Compras.gov.br**: Contratos e licitações
- **Portal da Transparência**: Dados de contratos
- **Formato**: JSON/CSV/ZIP
- **Paginação**: Automática com limite configurável

### 3. TransfereGov
- **API TransfereGov**: Convênios e transferências
- **Portal da Transparência**: Dados de convênios
- **Formato**: JSON/ZIP
- **Tratamento**: Específico para estrutura da API

## Como Usar

### Execução Completa (Recomendado)
```bash
# Windows (PowerShell)
.\run_final.ps1

# Linux/Mac
chmod +x run_poc.sh
./run_poc.sh
```

### Execução Manual por Etapas

1. **Aquisição de Dados**:
```bash
# Todas as fontes
python data_acquirer.py --source all --verbose

# Fonte específica
python data_acquirer.py --source siafi
python data_acquirer.py --source compras
python data_acquirer.py --source transferegov
```

2. **Integração de Dados**:
```bash
python integrate_data_simple.py
```

### Configuração Customizada
```bash
# Usar arquivo de configuração personalizado
python data_acquirer.py --config minha_config.json --source all
```

## Configuração (config.json)

O sistema usa um arquivo JSON para configurar URLs, headers e parâmetros:

```json
{
  "data_sources": {
    "siafi": {
      "name": "SIAFI - Sistema Integrado de Administração Financeira",
      "urls": [
        {
          "url": "https://portaldatransparencia.gov.br/download-de-dados/...",
          "format": "zip",
          "headers": {...}
        }
      ]
    }
  },
  "download_settings": {
    "timeout": 60,
    "max_retries": 3,
    "rate_limit_delay": 1.5
  }
}
```

## Tratamento de Erros

### Estratégia de Fallback
1. **Tentativa Primária**: URL oficial mais atual
2. **Tentativas Secundárias**: URLs alternativas configuradas
3. **Fallback Final**: Geração de dados de amostra estruturados

### Códigos de Erro Tratados
- **403 Forbidden**: User-Agent inadequado ou necessidade de autenticação
- **404 Not Found**: URL desatualizada ou recurso removido
- **429 Rate Limited**: Muitas requisições - aguarda automaticamente
- **Timeout**: Conexão lenta - retry automático
- **Connection Error**: Problemas de rede - retry automático

## Logs e Diagnóstico

### Arquivo de Log Principal
- **Nome**: `govhub_data_acquisition.log`
- **Conteúdo**: Todas as operações, erros e sucessos
- **Rotação**: Acumulativo (considerar rotação manual)

### Níveis de Log
- **INFO**: Operações normais e progressos
- **WARNING**: Falhas recuperáveis e fallbacks
- **ERROR**: Falhas críticas por fonte
- **DEBUG**: Detalhes técnicos (modo --verbose)

### Diagnóstico de Problemas

1. **Nenhum dado baixado**:
   - Verificar conectividade de internet
   - Verificar se URLs em config.json estão atuais
   - Verificar logs para códigos de erro específicos

2. **Erro 403 (Forbidden)**:
   - Portais podem estar bloqueando requisições automatizadas
   - Tentar atualizar User-Agent em config.json
   - Verificar se portal requer cadastro/API key

3. **Erro 404 (Not Found)**:
   - URLs podem ter mudado
   - Verificar documentação oficial dos portais
   - Atualizar URLs em config.json

4. **Downloads lentos**:
   - Aumentar timeout em config.json
   - Verificar conexão de internet
   - Considerar executar em horários de menor tráfego

## Saídas do Sistema

### Dados Brutos (`data/raw/`)
- `siafi_YYYY-MM-DD.csv`: Dados do SIAFI
- `contratos_YYYY-MM-DD.csv`: Dados de contratos
- `convenios_YYYY-MM-DD.csv`: Dados de convênios
- `*_amostra_*.csv`: Dados de fallback quando download falha

### Dados Processados (`data/processed/`)
- `integrated_poc_data.csv`: Dados integrados de todas as fontes
- `poc_summary.txt`: Relatório de resumo da execução

## Métricas e Monitoramento

### Indicadores de Sucesso
- **Taxa de Sucesso**: % de fontes que baixaram com êxito
- **Volume de Dados**: Tamanho total dos arquivos baixados
- **Tempo de Execução**: Duração total do processo
- **Tipos de Dados**: Real vs. Amostra

### Monitoramento de Performance
```powershell
# Verificar tamanho dos dados
Get-ChildItem "data\raw\*.csv" | Measure-Object -Property Length -Sum

# Verificar última execução
Get-Content "govhub_data_acquisition.log" | Select-Object -Last 50
```

## Próximos Passos

### Funcionalidades Planejadas
1. **Agendamento Automático**: Cron jobs / Task Scheduler
2. **Notificações**: Email/Slack quando execução falha
3. **Dashboard Web**: Interface para monitoramento
4. **Cache Inteligente**: Evitar re-downloads desnecessários
5. **Validação de Dados**: Verificação automática de qualidade

### Escalabilidade
1. **Paralelização**: Downloads simultâneos por fonte
2. **Armazenamento**: Integração com bancos de dados
3. **API própria**: Exposição dos dados integrados
4. **Containerização**: Docker para deployment

## Contribuição

Para contribuir com melhorias na aquisição de dados:

1. **URLs Atualizadas**: Monitore mudanças nos portais
2. **Novos Portais**: Adicione fontes em config.json
3. **Tratamento de Erros**: Melhore robustez para casos específicos
4. **Performance**: Otimize downloads e processamento

## Suporte

- **Logs**: Sempre verificar `govhub_data_acquisition.log`
- **Configuração**: Validar `config.json` está correto
- **Conectividade**: Testar URLs manualmente no navegador
- **Dependências**: Verificar `requirements.txt` está atualizado
