# Gov-Hub: Integração de Dados Governamentais

## Visão Geral

O Gov-Hub é uma Prova de Conceito (PoC) que demonstra a integração de dados de múltiplos sistemas estruturantes do governo federal brasileiro em uma base consolidada para análise pelo IPEA.

**IMPORTANTE**: Esta versão foi otimizada para funcionar com Python 3.13 no Windows, usando apenas bibliotecas nativas do Python para máxima compatibilidade.

## Arquitetura Simplificada

- **data_acquirer_simple.py**: Gera dados de amostra simulando aquisição de APIs governamentais
- **integrate_data_simple.py**: Integra os dados usando campos-chave comuns
- **Scripts PowerShell**: Automatizam configuração e execução no Windows

## Fontes de Dados (Simuladas na PoC)

| Sistema | Campos-Chave | Descrição |
|---------|--------------|-----------|
| SIAFI | codigo_ug, numero_empenho | Execução orçamentária |
| Compras.gov.br | uasg, id_contrato | Contratos e licitações |
| TransfereGov | codigo_siafi, convenio | Convênios e transferências |

## Como Executar

### Opção 1: Execução Completa
```powershell
# 1. Configurar ambiente
.\setup_final.ps1

# 2. Executar PoC
.\run_final.ps1

# 3. Validar resultados
.\validate_final.ps1
```

### Opção 2: Execução Manual
```powershell
# Criar dados de amostra
python data_acquirer_simple.py --source all

# Integrar dados
python integrate_data_simple.py

# Verificar resultados
Get-Content data\processed\poc_summary.txt
```

## Resultados

A PoC gera dois arquivos principais:

1. **data/processed/integrated_poc_data.csv**: Dataset integrado
2. **data/processed/poc_summary.txt**: Relatório detalhado da execução

### Exemplo de Saída
```
=== Resumo da Integração de Dados ===

Fontes de Dados:
- SIAFI: 5 registros
- Compras.gov.br: 5 registros
- TransfereGov: 5 registros

Resultados da Integração:
- Total de registros integrados: 5
- Correspondências SIAFI-Compras: 5
- Correspondências SIAFI-TransfereGov: 5

Taxa de Correspondência:
- SIAFI-Compras: 100.0%
- SIAFI-TransfereGov: 100.0%

Status: INTEGRAÇÃO CONCLUÍDA COM SUCESSO!
```

## Estrutura do Projeto

```
gov-hub/
├── data/
│   ├── raw/           # Dados brutos (CSVs de amostra)
│   └── processed/     # Dados integrados e relatórios
├── docs/              # Documentação
├── .github/workflows/ # Pipelines CI/CD
├── data_acquirer_simple.py    # Aquisição de dados
├── integrate_data_simple.py   # Integração de dados
├── setup_final.ps1           # Configuração do ambiente
├── run_final.ps1             # Execução da PoC
└── validate_final.ps1        # Validação do projeto
```

## Tecnologias Utilizadas

- **Python 3.13**: Linguagem principal
- **Bibliotecas nativas**: csv, json, pathlib, logging
- **PowerShell**: Automação para Windows
- **GitHub Actions**: CI/CD

## Diferenças desta Versão

Esta versão foi especificamente adaptada para:

1. **Compatibilidade com Python 3.13**: Eliminou dependências problemáticas (pandas, numpy)
2. **Execução no Windows**: Scripts PowerShell nativos
3. **Dados de Amostra**: Simula aquisição real de APIs para demonstração
4. **Simplicidade**: Foco na lógica de integração sem complexidades desnecessárias

## Próximos Passos

Para uma implementação em produção, considere:

1. Integração real com APIs governamentais
2. Uso de bibliotecas especializadas (pandas) quando disponíveis
3. Implementação de cache e otimizações de performance
4. Expandir cobertura de fontes de dados

## Suporte

Este projeto foi testado em:
- Windows 11
- Python 3.13.1
- PowerShell 5.1+

Para problemas ou dúvidas, consulte os logs gerados pelos scripts ou o arquivo `poc_summary.txt`.
