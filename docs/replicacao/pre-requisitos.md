# Pré-requisitos para Replicação do Gov Hub BR

Antes de iniciar o processo de replicação da plataforma Gov Hub BR em outro órgão público, é importante garantir que alguns pré-requisitos técnicos e operacionais estejam atendidos. Esta seção apresenta os componentes essenciais de infraestrutura, as tecnologias utilizadas no projeto e os conhecimentos recomendados para as equipes envolvidas.

---

## 🧱 Requisitos de Infraestrutura

A plataforma foi construída para funcionar em ambientes locais ou em nuvem, utilizando contêineres Docker e K8s para facilitar a instalação e padronizar ambientes. O ideal é contar com servidores dedicados (ou máquinas virtuais) organizados por função.

> Alternativamente, todo o stack pode ser executado com `docker-compose` em um único ambiente para fins de testes ou prototipação.

---

## 🔧 Tecnologias Utilizadas

Abaixo, a lista das tecnologias principais empregadas na arquitetura da plataforma:

| Tecnologia            | Função                                                    | Documentação Oficial                                  |
|-----------------------|-----------------------------------------------------------|--------------------------------------------------------|
| Apache Airflow        | Orquestração e agendamento de pipelines (DAGs)           | <https://airflow.apache.org/>                           |
| DBT (Data Build Tool) | Transformação e modelagem de dados                       | <https://docs.getdbt.com/>                              |
| PostgreSQL            | Armazenamento relacional e data warehouse                 | <https://www.postgresql.org/docs/>                      |
| Apache Superset       | Criação de dashboards e visualizações interativas         | <https://superset.apache.org/>                          |
| Docker                | Padronização de ambiente e deploy em containers           | <https://docs.docker.com/>                              |
| Astronomer Cosmos     | Integração entre DBT e Airflow                            | <https://github.com/astronomer/astronomer-cosmos>       |
| Kubernetes (K8s)      | Orquestração de contêineres e escalabilidade              | <https://kubernetes.io/docs/>                           |

---

## 👨‍💻 Conhecimentos Técnicos Recomendados

Embora a plataforma tenha sido pensada para ser reutilizável, alguns conhecimentos são importantes para facilitar a implantação e manutenção do projeto:

- **Python** (nível básico a intermediário): para leitura e edição das DAGs no Airflow.
- **SQL** (nível intermediário): para trabalhar com os modelos DBT e análises no Superset.
- **Conceitos de ETL/ELT e modelagem de dados**: para adaptar os fluxos às regras de negócio do órgão.
- **Conhecimento básico em APIs REST**: para configurar e consumir dados de sistemas estruturantes.

---

## 🔒 Considerações sobre Acesso a APIs

Nem todas as APIs públicas permitem acesso irrestrito. Algumas exigem:

- **Certificado digital A1/A3**
- **Token de autenticação gerado por sistemas internos**
- **Liberação específica por parte da equipe responsável pela API**

> Exemplo prático: durante os testes com dados do IBAMA, o acesso foi limitado por exigência de certificado digital. Portanto, o ideal é iniciar com APIs públicas e abertas, como as do [ComprasGov](https://compras.dados.gov.br) ou [TransfereGov](https://www.gov.br/pt-br/servicos/apresentar-propostas-de-transferencias-voluntarias).

---

Com esses pré-requisitos atendidos, é possível iniciar a implantação da estrutura base do Gov Hub BR no órgão desejado.
