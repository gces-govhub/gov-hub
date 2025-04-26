# Integração de Dados

Este documento detalha o pipeline de **ETL** implementado no Gov Hub BR, abrangendo desde a extração de dados via Apache Airflow até a transformação com DBT e a carga no PostgreSQL. O foco principal é a obtenção de dados das APIs governamentais, seu tratamento até a camada *Silver* e a organização no Data Warehouse.

---

## 1. Extração de Dados com Apache Airflow

### 1.1. Configuração de Conexões e Variáveis

- Defina conexões no Airflow (`Admin > Connections`) para cada API, se aplicável.

- Use `Variables` para parâmetros genéricos:
  - `api_timeout` (em segundos)
  - `retry_attempts`

### 1.2. Estrutura das DAGs

Exemplo de DAG para extração de um órgão:

```python
import logging
import yaml
from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from postgres_helpers import get_postgres_conn
from cliente_contratos import ClienteContratos
from cliente_postgres import ClientPostgresDB


@dag(
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "owner": "Davi",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["contratos_api"],
)
def api_contratos_dag() -> None:
    """DAG para buscar e armazenar contratos por órgão definido."""

    @task
    def fetch_and_store_contratos() -> None:
        logging.info("[contratos_ingest_dag.py] Iniciando extração")

        orgao_alvo = Variable.get("airflow_orgao", default_var=None)
        if not orgao_alvo:
            logging.error("Variável airflow_orgao não definida!")
            raise ValueError("airflow_orgao não definida")

        orgaos_config_str = Variable.get("airflow_variables", default_var="{}")
        orgaos_config = yaml.safe_load(orgaos_config_str)

        codigos_ug = orgaos_config.get(orgao_alvo, {}).get("codigos_ug", [])

        if not codigos_ug:
            logging.warning(f"Nenhum código UG encontrado para o órgão '{orgao_alvo}'")
            return

        api = ClienteContratos()
        postgres_conn_str = get_postgres_conn()
        db = ClientPostgresDB(postgres_conn_str)

        for ug_code in codigos_ug:
            logging.info(f"Buscando contratos para UG: {ug_code}")
            contratos = api.get_contratos_by_ug(ug_code)

            if contratos:
                logging.info(f"Inserindo contratos da UG {ug_code} no schema compras_gov")
                db.insert_data(
                    contratos,
                    "contratos",
                    conflict_fields=["id"],
                    primary_key=["id"],
                    schema="compras_gov",
                )
            else:
                logging.warning(f"Nenhum contrato encontrado para UG {ug_code}")

    trigger_contratos_inativos = TriggerDagRunOperator(
        task_id="trigger_contratos_inativos",
        trigger_dag_id="api_contratos_inativos_dag",
        wait_for_completion=False,
    )

    fetch_and_store_contratos() >> trigger_contratos_inativos


dag_instance = api_contratos_dag()

```  

### 1.3. Boas Práticas

- Evite DAGs monolíticas: crie funções e subDAGs para cada recurso.
- Implemente alertas para falhas críticas.
- Documente endpoints e versões de API.

---

## 2. Transformação e Modelagem com DBT

### 2.1. Estrutura do Projeto

### 2.2. Modelagem

## 3. Carga e Organização no PostgreSQL

### 3.1. Convenções de Schema e Tabelas

### 3.2. Monitoramento

- Configure alertas de consumo de espaço e performance.
- Utilize métricas do PostgreSQL para identificar gargalos.

---

## 4. Observações e Limitações

- APIs que requerem certificado digital A1/A3 podem exigir configuração adicional em servidores Airflow.
- Algumas fontes limitam a quantidade de requisições diárias.
- A camada Gold depende de regras de negócio específicas e é disponibilizada como template.

---
