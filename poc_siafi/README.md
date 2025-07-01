# 🏛️ PoC SIAFI - Scripts Python Organizados

Esta pasta contém todos os scripts Python relacionados à Prova de Conceito (PoC) do SIAFI no projeto Gov-Hub.

## 📋 Scripts Principais

### 🎯 Scripts de Execução Principal
- **`run_poc_siafi_complete.py`** - Script principal da PoC com dados reais do Portal da Transparência
- **`run_siafi_poc.py`** - Execução da PoC com dados locais/existentes

### 📡 Scripts de Coleta de Dados
- **`collect_real_siafi.py`** - Coleta dados reais do SIAFI via API oficial
- **`collect_real_gov_data.py`** - Coleta dados de múltiplas fontes governamentais
- **`acquire_real_siafi.py`** - Aquisição específica de dados SIAFI
- **`siafi_acquirer.py`** - Sistema de aquisição de dados SIAFI
- **`data_acquirer.py`** - Sistema principal de aquisição de dados

### 🔄 Scripts de Processamento e Integração
- **`integrate_data.py`** - Sistema principal de integração de dados
- **`integrate_data_simple.py`** - Versão simplificada para compatibilidade

### 🔧 Scripts de Utilitários
- **`organize_siafi.py`** - Organiza e estrutura dados existentes
- **`generate_realistic_siafi.py`** - Gera dados sintéticos realistas para testes

### 🧪 Scripts de Teste e Validação
- **`validate_poc_complete.py`** - Validação completa do sistema (96.7% aprovação)
- **`validate_poc.py`** - Validação básica da PoC
- **`demo_api_real.py`** - Demonstração e teste da API real
- **`test_api_direct.py`** - Teste direto das APIs governamentais
- **`explore_api.py`** - Exploração das capacidades da API

## 🚀 Como Executar

### Execução Rápida (Recomendada)
```bash
# Para dados reais (requer chave de API)
python run_poc_siafi_complete.py

# Para dados locais
python run_siafi_poc.py
```

### Execução Passo a Passo
```bash
# 1. Organizar dados existentes
python organize_siafi.py

# 2. Coletar dados reais (opcional)
python collect_real_siafi.py

# 3. Executar PoC completa
python run_poc_siafi_complete.py

# 4. Validar resultados
python validate_poc_complete.py
```

## 📊 Resultados

Os resultados são salvos em:
- `../data/poc_siafi/dados_brutos/` - Dados originais coletados
- `../data/poc_siafi/dados_processados/` - Dados processados e amostras
- `../data/poc_siafi/relatorios/` - Relatórios consolidados

## 🔑 Configuração da API

Para usar dados reais, configure a chave da API:

```bash
# Arquivo .env na raiz do projeto
PORTAL_TRANSPARENCIA_API_KEY=sua_chave_aqui
```

Obtenha sua chave em: http://www.portaldatransparencia.gov.br/api-de-dados/cadastrar-email

## 📈 Status Atual

✅ **Sistema 100% Funcional**  
✅ **96.7% de Aprovação nos Testes**  
✅ **Capacidade de Big Data Validada**  
✅ **Dados Reais Processados com Sucesso**

Para documentação completa, consulte: `../DOCUMENTACAO_POC_CONSOLIDADA.md`
