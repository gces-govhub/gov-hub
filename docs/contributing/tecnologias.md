# tecnologias utilizadas

esta página apresenta as principais tecnologias adotadas no desenvolvimento do gov hub br. cada uma delas cumpre um papel específico na arquitetura do projeto, contribuindo para a eficiência, escalabilidade e transparência da plataforma.

---

## apache airflow

o apache airflow é responsável pelo gerenciamento e orquestração dos nossos pipelines de dados (dags). ele permite o agendamento, monitoramento e execução de tarefas complexas de forma visual e escalável.

🔗 link para a documentação do airflow: [https://airflow.apache.org/](https://airflow.apache.org/)

---

## dbt (data build tool)

o dbt é utilizado para transformar, modelar e documentar os dados dentro do ambiente analítico. ele facilita a criação de pipelines de transformação reutilizáveis e versionáveis.

🔗 link para a documentação do dbt: [https://docs.getdbt.com/](https://docs.getdbt.com/)

---

## apache superset

utilizamos o apache superset para criar dashboards interativos e visualizações que facilitam a análise dos dados processados. ele permite que gestores públicos explorem as informações de forma simples e eficiente.

🔗 link para a documentação do superset: [https://superset.apache.org/](https://superset.apache.org/)

---

## postgresql

o postgresql é o banco de dados relacional utilizado para armazenar dados estruturados. sua robustez e compatibilidade com ferramentas open-source o tornam ideal para o projeto.

🔗 link para a documentação do postgresql: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

---

## docker

o docker é usado para conteinerizar a aplicação, garantindo ambientes consistentes em diferentes etapas do desenvolvimento, testes e produção. ele também facilita a colaboração entre equipes.

🔗 link para a documentação do docker: [https://docs.docker.com/](https://docs.docker.com/)

---

## mkdocs

o mkdocs é a ferramenta utilizada para criar e manter a documentação oficial do projeto. ele permite gerar páginas estáticas a partir de arquivos markdown de forma rápida e organizada.

🔗 link para a documentação do mkdocs: [https://www.mkdocs.org/](https://www.mkdocs.org/)

---

## astronomer cosmos

o cosmos é uma extensão do astronomer para integração entre dbt e airflow. utilizamos essa ferramenta para orquestrar pipelines dbt dentro do ambiente do airflow de forma nativa e eficiente.

🔗 link para a documentação do cosmos: [https://github.com/astronomer/astronomer-cosmos](https://github.com/astronomer/astronomer-cosmos)

---
