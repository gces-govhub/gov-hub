# arquitetura e infraestrutura

Esta seção apresenta a visão geral da arquitetura do govhub, os principais componentes da infraestrutura, bem como orientações sobre configuração e escalabilidade. o objetivo é fornecer uma compreensão clara de como os dados fluem pela plataforma, desde sua origem até a visualização.

---

## visão geral da arquitetura

a arquitetura do gov hub br é baseada em uma estrutura de dados que segue os princípios do data lakehouse, utilizando camadas de processamento (bronze, silver e gold) para garantir qualidade e governança dos dados.

o fluxo básico pode ser representado assim:

origens de dados → airflow (orquestração) → dbt (transformação)
→ data warehouse (bronze/silver/gold) → superset (visualização)

---

## componentes da infraestrutura

### 🔧 apache airflow

- atua como motor de orquestração de tarefas (dags), permitindo agendamento, dependência entre processos e monitoramento em tempo real.
- cada fluxo de dados (etl) é representado como uma DAG.
- integração nativa com docker e astronomer cosmos.

### 🔧 dbt (data build tool)

- responsável pela transformação e modelagem dos dados no ambiente analítico.
- realiza versionamento de modelos, documentação automática e validação de dados.
- opera sobre dados brutos (bronze) e gera tabelas intermediárias (silver) e finais (gold).

### 🔧 astronomer cosmos

- extensão que integra airflow e dbt de forma nativa.
- permite executar modelos dbt como tarefas dentro das dags do airflow.
- reduz a complexidade da integração entre transformação e orquestração.

### 🛢️ data warehouse (postgresql)

- estrutura de armazenamento de dados dividida em três camadas:
  - **bronze**: dados brutos, diretamente extraídos das fontes.
  - **silver**: dados limpos e tratados, prontos para análise.
  - **gold**: dados agregados, otimizados para consumo por ferramentas de BI.
- atualmente implementado com postgresql, mas preparado para escalar para soluções cloud (ex: redshift, bigquery).

### 📊 ferramentas de bi

- **apache superset**: plataforma open-source utilizada para criar dashboards interativos.

---

## configuração da infraestrutura

### servidores e ambiente

- o projeto pode ser executado localmente com docker-compose ou em ambientes cloud.
- estrutura recomendada:
  - servidor para orquestração (airflow + cosmos)
  - servidor para banco de dados (postgres)
  - servidor para bi (superset)

### permissões e segurança

- acesso ao banco de dados deve ser controlado com usuários distintos para leitura, escrita e administração.
- airflow deve se conectar ao banco com usuário restrito (ex: `etl_user`).
- superset deve se conectar com um usuário apenas-leitura.
- recomenda-se a utilização de `.env` ou secrets manager para variáveis sensíveis.

### conectores

- airflow e dbt usam conexões configuráveis por URI.
- exemplo de conexão airflow → postgres:

postgres://etl_user:senha@host:5432/db

- superset se conecta ao banco via SQLAlchemy URI configurada na interface web.

---

## escalabilidade

o gov hub br foi desenhado para operar com grandes volumes de dados e pode escalar de forma horizontal e modular:

- **airflow** pode ser executado com múltiplos workers em um ambiente Kubernetes ou Celery.
- **dbt** suporta execução paralela e pode ser integrado com cloud warehouses altamente escaláveis.
- **postgres** pode ser substituído por soluções como redshift, snowflake ou bigquery conforme a demanda.
- dashboards em superset podem ser otimizados com caching e queries materializadas.

---

## considerações finais

a arquitetura modular do gov hub br permite flexibilidade para evoluir conforme as necessidades dos órgãos públicos, mantendo uma base sólida de governança e performance.
