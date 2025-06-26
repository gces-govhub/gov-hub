# Prova de Conceito (POC) - Gov-Hub

## 1. Objetivo

Esta Prova de Conceito (POC) foi desenvolvida para validar a viabilidade técnica de coletar, integrar e processar dados de diferentes sistemas governamentais, servindo como a base para o projeto Gov-Hub.

## 2. Análise do Código

* **Script Principal:** O script principal da POC é implementado como uma DAG do Airflow localizada no diretório `airflow/dags/`. A DAG realiza a extração de dados da API de Contratos Governamentais.

* **Fontes de Dados:**
    * APIs dos sistemas governamentais estruturantes:
        * SIAFI (Sistema Integrado de Administração Financeira)
        * Compras Gov
        * TransfereGov
    * Os dados são coletados através de chamadas REST às APIs públicas destes sistemas

* **Campos de Integração:**
    * A integração dos dados é realizada utilizando os seguintes campos-chave:
        * ID do contrato
        * Código da Unidade Gestora (UG)
        * IDs de empenho
    * As operações de junção são realizadas nas camadas Silver e Gold do data warehouse

## 3. Guia de Execução Rápida

Para reproduzir esta POC localmente, siga os passos:

1. **Clone o repositório e navegue até a pasta raiz.**

2. **(Opcional) Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure as variáveis do Airflow:**
    - No menu Admin > Variables do Airflow, configure:
        - `airflow_orgao`: Nome do órgão alvo
        - `api_timeout`: Timeout para chamadas de API (em segundos)
        - `retry_attempts`: Número de tentativas em caso de falha

5. **Execute os serviços via Docker:**
    ```bash
    docker-compose up -d
    ```

6. **Acesse as interfaces:**
    - Airflow: http://localhost:8080
    - Jupyter: http://localhost:8888
    - Superset: http://localhost:8088

## 4. Validação do Resultado

* **Critério de Sucesso:** A POC é considerada finalizada quando:
    1. Os dados são extraídos com sucesso das APIs governamentais
    2. As transformações nas camadas Bronze e Silver são concluídas
    3. Os dados são disponibilizados para consulta no PostgreSQL

* **Snippet de Validação Rápida:**
    ```python
    import pandas as pd
    from sqlalchemy import create_engine

    # Conecta ao banco de dados
    engine = create_engine('postgresql://usuario:senha@localhost:5432/govhub')

    # Verifica os dados importados
    df = pd.read_sql_query('SELECT * FROM compras_gov.contratos LIMIT 5', engine)
    print(df.head())
    ```

## 5. Arquitetura da POC

A POC implementa uma arquitetura em camadas:

1. **Extração (Apache Airflow)**
   - Orquestração dos pipelines de dados via DAGs
   - Gestão de dependências e retry em caso de falhas
   - Monitoramento da execução

2. **Transformação (DBT)**
   - Modelagem dos dados em camadas (Bronze → Silver → Gold)
   - Documentação automática dos modelos
   - Testes de qualidade dos dados

3. **Armazenamento (PostgreSQL)**
   - Organização em schemas por domínio
   - Versionamento dos dados
   - Otimização de queries

4. **Visualização (Apache Superset)**
   - Dashboards interativos
   - Exploração ad-hoc
   - Compartilhamento de análises

## 6. Limitações e Próximos Passos

* **Limitações Identificadas:**
    - APIs podem requerer certificados digitais
    - Algumas fontes possuem limites de requisições
    - Necessidade de tratamento específico por órgão

* **Próximos Passos:**
    1. Implementar autenticação via certificado digital
    2. Expandir para outros sistemas estruturantes
    3. Desenvolver modelos Gold específicos por caso de uso
    4. Criar templates de dashboards para análise
