# Arquitetura e Infraestrutura

Esta seção apresenta uma visão geral da arquitetura do **GovHubBR**, seus principais componentes de infraestrutura e orientações sobre configuração e escalabilidade. O objetivo é oferecer uma compreensão clara de como os dados fluem pela plataforma, desde sua origem até a visualização.

---

## 🌍 Visão Geral da Arquitetura

A arquitetura do GovHubBR segue os princípios de **data lakehouse**, com camadas de processamento **Bronze**, **Silver** e **Gold**, garantindo qualidade, rastreabilidade e governança de dados.

**Fluxo simplificado de dados:**

```
Origens de Dados → Apache Airflow (Orquestração) → DBT (Transformação)
 → Data Warehouse (Bronze / Silver / Gold) → Superset (Visualização)
```

---

## 🛠️ Componentes da Infraestrutura

### 🔧 Apache Airflow

- Motor de orquestração dos pipelines de dados (DAGs).
- Gerencia dependências, agendamentos e monitoramento de execução.
- Integração nativa com Docker e **Astronomer Cosmos**.

### 🔧 DBT (Data Build Tool)

- Responsável pela transformação e modelagem dos dados.
- Versionamento, documentação automática e validação de modelos.
- Atua nas camadas Bronze (bruta), Silver (tratada) e Gold (agregada).

### 🔧 Astronomer Cosmos

- Extensão que integra DBT diretamente ao Airflow.
- Executa modelos DBT como tarefas dentro das DAGs.
- Reduz complexidade e melhora manutenção dos pipelines.

### 📃 Data Warehouse (PostgreSQL)

- Estrutura dividida em:
  - **Bronze**: dados brutos, extraídos diretamente das fontes.
  - **Silver**: dados tratados e padronizados para análise.
  - **Gold**: dados agregados e prontos para consumo por BI.
- Atualmente utiliza PostgreSQL, com suporte para Redshift, BigQuery, etc.

### 📊 Ferramentas de BI

- **Apache Superset**: utilizado para visualização de dados por meio de dashboards interativos e exploratórios.

---

## 🚀 Configuração da Infraestrutura

### 🏢 Servidores e Ambiente

- Execução local via Docker Compose ou em ambientes cloud.
- Estrutura recomendada:
  - Servidor para orquestração (Airflow + Cosmos)
  - Servidor de banco de dados (PostgreSQL)
  - Servidor de BI (Superset)

### 🔒 Permissões e Segurança

- Controle de acesso com usuários distintos:
  - Leitura, escrita e administração.
  - Airflow usa `etl_user` com acesso restrito.
  - Superset utiliza usuário somente leitura.
- Uso de arquivos `.env` ou secret managers para variáveis sensíveis.

### 🔗 Conectores

- Airflow e DBT usam conexões URI:

```text
postgres://etl_user:senha@host:5432/db
```

- Superset se conecta via URI SQLAlchemy configurada na interface.

---

## ⚖️ Escalabilidade

O GovHubBR é desenhado para lidar com grandes volumes de dados, com opções de escalabilidade horizontal e modular:

- **Airflow** pode operar com múltiplos workers via Kubernetes ou Celery.
- **DBT** suporta execução paralela e integração com cloud warehouses.
- **PostgreSQL** pode ser substituído por Redshift, Snowflake ou BigQuery.
- **Superset** pode ser otimizado com caching e queries materializadas.

---

## 🔍 Considerações Finais

A arquitetura modular do **GovHubBR** garante flexibilidade e capacidade de evoluir conforme as necessidades dos órgãos públicos, mantendo um alto padrão de governança, performance e escalabilidade.
