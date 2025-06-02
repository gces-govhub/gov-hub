# Tecnologias Utilizadas

Esta página apresenta as principais tecnologias adotadas no desenvolvimento do **GovHubBR**. Cada uma delas exerce um papel estratégico na arquitetura do projeto, contribuindo para sua eficiência, escalabilidade e transparência.

---

## 🛠 Apache Airflow

Responsável pela **orquestração dos pipelines de dados (DAGs)**, o Apache Airflow permite o agendamento, monitoramento e execução de tarefas complexas de forma visual, escalável e modular.

🔗 [Documentação oficial do Airflow](https://airflow.apache.org/)

---

## 🧱 DBT (Data Build Tool)

Utilizamos o DBT para **transformação e modelagem de dados** em nosso ambiente analítico. Ele facilita a criação de pipelines reutilizáveis, versionáveis e com boa rastreabilidade.

🔗 [Documentação oficial do DBT](https://docs.getdbt.com/)

---

## 📊 Apache Superset

O Superset é a ferramenta escolhida para **visualização de dados e criação de dashboards** interativos. Ele permite que usuários explorem os dados de forma intuitiva e responsiva.

🔗 [Documentação oficial do Superset](https://superset.apache.org/)

---

## 🗄 PostgreSQL

Banco de dados relacional utilizado para **armazenamento de dados estruturados**. Sua robustez, performance e integração com ferramentas open-source o tornam ideal para projetos governamentais.

🔗 [Documentação oficial do PostgreSQL](https://www.postgresql.org/docs/)

---

## 📦 Docker

Utilizado para **containerização da aplicação**, garantindo consistência entre ambientes de desenvolvimento, testes e produção. Também facilita a escalabilidade e integração entre equipes.

🔗 [Documentação oficial do Docker](https://docs.docker.com/)

---

## 📚 MkDocs

Ferramenta usada para **gerar a documentação estática** do projeto a partir de arquivos Markdown. Ela possibilita uma apresentação organizada, responsiva e fácil de manter.

🔗 [Documentação oficial do MkDocs](https://www.mkdocs.org/)

---

## 🚀 Astronomer Cosmos

Extensão do Astronomer que permite a **integração nativa entre DBT e Apache Airflow**. Utilizamos o Cosmos para orquestrar pipelines DBT dentro do ambiente do Airflow de forma padronizada e eficiente.

🔗 [Repositório oficial do Cosmos](https://github.com/astronomer/astronomer-cosmos)

---
