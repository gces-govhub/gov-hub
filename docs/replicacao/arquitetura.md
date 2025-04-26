# Arquitetura da Solução

A arquitetura da plataforma Gov Hub BR foi elaborada para promover modularidade, escalabilidade e adoção de tecnologias de código aberto, assegurando flexibilidade adaptativa às demandas específicas de diferentes órgãos públicos, sem comprometer os requisitos de governança e qualidade de dados.

---

## Visão Geral

O design adota o paradigma Lakehouse, estruturado em três camadas de processamento de dados:

    Fontes de dados (APIs)
    ↓
    Apache Airflow (orquestração e extração)
    ↓
    DBT (transformação e modelagem)
    ↓
    PostgreSQL (armazenamento em Bronze, Silver e Gold)
    ↓
    Apache Superset (visualização e relatórios)

---

## Componentes Principais

### Apache Airflow

Disponibiliza orquestração robusta de fluxos de trabalho (ETL) por meio de Grafos Acíclicos Dirigidos (DAGs), coordenando a extração automatizada de dados brutos a partir das APIs governamentais, com registro de dependências e monitoramento em tempo real.

### DBT (Data Build Tool)

Responsável pela aplicação de transformações programáticas em SQL, modelagem de dados e geração de artefatos nas camadas Silver e Gold. Facilita versionamento, testes automatizados e documentação contínua dos modelos.

### Astronomer Cosmos

Extensão que integra nativamente o DBT ao Airflow, habilitando a execução orquestrada de modelos DBT dentro das DAGs e simplificando a gestão de dependências entre tarefas de transformação.

### PostgreSQL

Serviço de armazenamento relacional configurado como um Data Warehouse, organizado em três domínios:

- **Bronze:** repositório de dados brutos, sem alterações.
- **Silver:** dados limpos, validados e normalizados para análises exploratórias.
- **Gold:** dados agregados e estruturados conforme regras de negócio específicas.

### Apache Superset

Ferramenta de business intelligence que consome a camada Gold, permitindo a construção de painéis interativos e relatórios analíticos parametrizáveis, promovendo a disseminação de insights corporativos.

---

## Organização em Camadas

- **Bronze:** preservação integral dos registros originais, garantindo auditabilidade.
- **Silver:** normalização, enriquecimento e unificação de conjuntos de dados.
- **Gold:** consolidação final e aplicação de lógica de negócio para suporte à tomada de decisão.

---

## Flexibilidade e Escalabilidade

A pilha pode ser executada localmente via Docker Compose para validações iniciais, e dimensionada para ambientes de produção em nuvem, incluindo:

- Execução distribuída do Airflow em Kubernetes ou CeleryExecutor.
- Substituição de PostgreSQL por soluções analíticas escaláveis (Redshift, Snowflake, BigQuery).
- Otimizações de cache e materializações no Superset para grandes volumes de dados.

---

Para maior detalhamento do processo de extração, transformação e carga de dados, consulte a seção **Integração de Dados**.
