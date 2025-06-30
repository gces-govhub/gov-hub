# Gov-Hub - Configuração do Projeto

Este diretório centraliza todas as configurações do projeto Gov-Hub.

## Arquivos de Configuração

### `config.json`
Configuração principal do projeto contendo:
- **Fontes de dados**: URLs e configurações das APIs governamentais
- **Parâmetros de conexão**: Headers HTTP, timeouts, retry
- **Estrutura de dados**: Schema e validações
- **Configurações de processamento**: Chunk sizes, limites

### `legacy/config.json`
Versão anterior do arquivo de configuração (backup).

### `giscus.json`
Configurações para sistema de comentários (se aplicável).

## Estrutura do Projeto Atual

```
gov-hub/
├── config/                 # Configurações (você está aqui)
│   ├── config.json        # Configuração principal
│   ├── README.md          # Este arquivo
│   └── legacy/            # Configurações antigas
├── data/                  # Dados processados
│   ├── processed/         # Dados finais integrados
│   ├── raw/              # Dados brutos das APIs
│   └── temp/             # Dados temporários
├── docs/                 # Documentação completa
│   ├── README_POC_COMPLETO.md # Documentação consolidada
│   ├── contributing/     # Guias de contribuição
│   └── guias/           # Guias de uso
├── legacy/              # Código legado (backup)
├── logs/                # Arquivos de log
├── scripts/             # Scripts de automação
├── src/                 # Código fonte principal
└── tests/               # Testes automatizados
```

## Fontes de Dados Configuradas

### SIAFI (Sistema Integrado de Administração Financeira)
- **URL**: Portal da Transparência - Despesas
- **Formato**: ZIP/CSV
- **Dados**: Execução orçamentária e despesas federais

### Compras.gov
- **URL**: API de contratos governamentais
- **Formato**: JSON/CSV
- **Dados**: Contratos e licitações

### TransfereGov
- **URL**: API de transferências voluntárias
- **Formato**: JSON/CSV
- **Dados**: Transferências e convênios

## Configurações de Performance

- **Timeout**: 30 segundos por requisição
- **Retry**: 3 tentativas com backoff exponencial
- **Chunk Size**: 1000 registros por processamento
- **Rate Limiting**: Respeitado conforme especificações das APIs

## Variáveis de Ambiente

Para configurações sensíveis, use o arquivo `.env`:

```bash
# Banco de Dados
DB_HOST=localhost
DB_PORT=5432
DB_NAME=govhub
DB_USER=user
DB_PASSWORD=password

# APIs
API_TIMEOUT=30
RETRY_ATTEMPTS=3
CHUNK_SIZE=1000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/govhub.log
```

## Como Configurar

1. **Configuração inicial**:
   ```bash
   cp .env.example .env
   # Edite .env com suas configurações específicas
   ```

2. **Verificar configuração**:
   ```bash
   python -c "import json; print(json.load(open('config/config.json'))['data_sources'].keys())"
   ```

3. **Testar conectividade**:
   ```bash
   python data_acquirer.py --test-only
   ```

## Segurança

- ❌ **NÃO** commite senhas ou tokens no `config.json`
- ✅ Use variáveis de ambiente para informações sensíveis
- ✅ Mantenha logs locais fora do controle de versão
- ✅ Use HTTPS sempre que possível

## Suporte

Consulte a [documentação completa](../docs/README_POC_COMPLETO.md) para mais detalhes sobre configuração e uso.
