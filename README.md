# Gov-Hub: PoC SIAFI - Análise de Dados do Sistema Integrado de Administração Financeira

## 🎯 Status do Projeto: PoC SIAFI VALIDADA ✅

**O Gov-Hub agora foca exclusivamente no processamento e análise de dados do SIAFI (Sistema Integrado de Administração Financeira), fornecendo insights sobre a execução orçamentária do governo federal.**

### 🏆 Conquistas da PoC SIAFI (30/06/2025)
- ✅ **Pipeline SIAFI** 100% funcional e organizado
- ✅ **Dados de despesas** do Portal da Transparência processados
- ✅ **Estrutura de dados** clara e bem documentada
- ✅ **Relatórios automáticos** de análise financeira
- ✅ **Código limpo** e focado em uma única fonte de dados

### 📋 Como Executar a PoC
1. **Instalar dependências**: `pip install -r requirements.txt`
2. **Executar PoC completa**: `python run_siafi_poc.py`
3. **Organizar dados existentes**: `python organize_siafi.py`
4. **Baixar novos dados**: `python siafi_acquirer.py`

### 📁 Estrutura de Dados
- `data/poc_siafi/dados_brutos/` - Dados originais do SIAFI
- `data/poc_siafi/dados_processados/` - Amostras e dados processados
- `data/poc_siafi/relatorios/` - Relatórios de análise e logs

---

## Sobre o Projeto

O Gov-Hub SIAFI é uma Prova de Conceito focada na coleta, processamento e análise de dados do Sistema Integrado de Administração Financeira (SIAFI) do governo federal. O projeto demonstra como automatizar a extração de dados do Portal da Transparência e gerar insights sobre a execução orçamentária.

## Objetivos da PoC SIAFI

- **Automatizar** a coleta de dados do SIAFI via Portal da Transparência
- **Processar** grandes volumes de dados de despesas públicas
- **Gerar** amostras e relatórios analíticos automaticamente
- **Organizar** dados em estrutura clara e reproduzível
- **Validar** a viabilidade técnica de integração com dados governamentais

## Pré-requisitos

- **Python 3.8+**: Para execução dos scripts
- **pip**: Para instalação das dependências

## 🚀 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone <repository-url>
cd gov-hub
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a PoC Completa
```bash
python run_siafi_poc.py
```

### 4. Scripts Individuais

- **Baixar novos dados SIAFI**: `python siafi_acquirer.py`
- **Organizar dados existentes**: `python organize_siafi.py`

## 📊 Resultados da PoC

Após a execução, você encontrará:

- **Dados Brutos**: CSVs originais do SIAFI organizados
- **Amostras**: Subconjuntos de dados para análise rápida  
- **Relatórios**: Análises automáticas e estatísticas descritivas
- **Logs**: Registros detalhados de execução

## 🛠 Estrutura de Arquivos

```
gov-hub/
├── siafi_acquirer.py          # Script principal de coleta SIAFI
├── organize_siafi.py          # Organizador de dados existentes
├── run_siafi_poc.py           # Executor da PoC completa
├── config/
│   └── siafi_config.json      # Configurações do SIAFI
└── data/
    └── poc_siafi/
        ├── dados_brutos/      # CSVs originais
        ├── dados_processados/ # Amostras e dados tratados
        └── relatorios/        # Análises e logs
```

## 🎯 Próximos Passos

- Expandir análises financeiras automatizadas
- Implementar visualizações de dados
- Integrar com outras fontes governamentais
- Desenvolver APIs para acesso aos dados processados

---

**Gov-Hub SIAFI** - Transformando dados do SIAFI em insights estratégicos para o governo federal.

