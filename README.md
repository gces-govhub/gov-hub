# Gov H## 🎯 Status do Projeto: PROTÓTIPO FUNCIONAL VALIDADO ✅

**O Gov-Hub superou suas metas iniciais e evoluiu de uma Prova de Conceito para um protótipo funcional capaz de processar dados governamentais reais em larga escala.**

### 🏆 Conquistas Recentes (26/06/2025)
- ✅ **48.912 registros reais** do SIAFI processados
- ✅ **39.7 MB** de dados do Portal da Transparência baixados
- ✅ **R$ 650+ bilhões** em despesas públicas analisadas
- ✅ **Pipeline completo** funcionando em < 2 minutos
- ✅ **Sistema de fallback** 100% operacional
- ✅ **Documentação consolidada** e projeto reorganizado

### 📋 Documentação Consolidada ⭐
- 📚 [**Documentação Completa da POC**](docs/poc/README_POC_COMPLETO.md) - **LEIA PRIMEIRO** - Tudo sobre o projeto em um só lugar
- 🚀 [**Guia de Início Rápido**](docs/getting-started.md) - Como começar a usar o projeto
- 👥 [**Guia de Contribuição**](docs/contributing/CONTRIBUTING.md) - Como contribuir com o projeto
- 📋 [**Índice de Documentação**](docs/INDICE_DOCUMENTACAO.md) - Guia completo de navegação
- 🗂️ [**Nova Estrutura**](ESTRUTURA_REORGANIZADA.md) - Organização do projetoma de Integração de Dados Governamentais

[![Contribua com o projeto 🚀](https://img.shields.io/badge/Contribua%20com%20o%20projeto-🚀-brightgreen)](CONTRIBUTING.md)
[![Status do Projeto](https://img.shields.io/badge/Status-Protótipo%20Funcional%20Validado-success)](RESUMO_EXECUTIVO_FINAL.md)
[![Última Execução](https://img.shields.io/badge/Última%20Execução-26%2F06%2F2025-blue)](RELATORIO_FINAL_EXECUCAO.md)
[![Dados Processados](https://img.shields.io/badge/SIAFI-48.912%20registros-orange)](RELATORIO_FINAL_EXECUCAO.md)

## 🎯 Status do Projeto: PROTÓTIPO FUNCIONAL VALIDADO ✅

**O Gov-Hub superou suas metas iniciais e evoluiu de uma Prova de Conceito para um protótipo funcional capaz de processar dados governamentais reais em larga escala.**

### 🏆 Conquistas Recentes (26/06/2025)
- ✅ **48.912 registros reais** do SIAFI processados
- ✅ **39.7 MB** de dados do Portal da Transparência baixados
- ✅ **R$ 650+ bilhões** em despesas públicas analisadas
- ✅ **Pipeline completo** funcionando em < 2 minutos
- ✅ **Sistema de fallback** 100% operacional

### 📋 Documentação Completa
- � [**Documentação Completa da POC**](docs/README_POC_COMPLETO.md) - Documentação consolidada e completa
- � [**Guia de Início Rápido**](docs/getting-started.md) - Como começar a usar o projeto
- � [**Guia de Contribuição**](docs/contributing/CONTRIBUTING.md) - Como contribuir com o projeto
- � [**Índice de Documentação**](docs/INDICE_DOCUMENTACAO.md) - Guia completo de navegação

---

## Sobre o projeto

O Gov Hub BR é uma iniciativa para enfrentar os desafios da fragmentação, redundância e inconsistências nos sistemas estruturantes do governo federal. O projeto busca transformar dados públicos em ativos estratégicos, promovendo eficiência administrativa, transparência e melhor tomada de decisão. A partir da integração de dados, gestores públicos terão acesso a informações qualificadas para subsidiar decisões mais assertivas, reduzir custos operacionais e otimizar processos internos. Além disso, a iniciativa fortalece a transparência governamental ao disponibilizar dados organizados para órgãos públicos e sociedade civil.

## Objetivos

O projeto busca automatizar processos e reduzir custos por meio da implementação de soluções open-source que facilitem a coleta, análise e visualização de dados. Também visa desenvolver capacidades técnicas e institucionais, oferecendo ferramentas para que gestores públicos utilizem os dados de forma eficiente e independente. A construção de uma infraestrutura tecnológica sustentável baseada em tecnologias escaláveis e flexíveis garante a longevidade da solução e sua adaptação a novas necessidades. Além disso, promove uma cultura organizacional voltada para dados, incentivando boas práticas de governança, segurança e transparência.

## Impactos esperados

A qualificação e integração de dados contribuem para a melhoria na qualidade das políticas públicas, permitindo que decisões sejam baseadas em informações concretas e alinhadas às necessidades da população. A redução da fragmentação de sistemas possibilita o aumento da eficiência administrativa, otimizando o uso de recursos e promovendo maior agilidade nos serviços prestados pelo governo. O fortalecimento da transparência governamental garante maior controle social e auditoria, ampliando a confiança da sociedade na administração pública.

## Tecnologias utilizadas

O projeto adota um stack tecnológico baseado em soluções open-source, incluindo Apache Airflow para orquestração de pipelines de dados, DBT para transformação e modelagem de informações, Apache Superset para visualização e exploração, PostgreSQL como banco de dados relacional e Docker para containerização e implantação. A escolha dessas tecnologias permite maior flexibilidade, escalabilidade e integração com diferentes sistemas governamentais.
- [Apache Airflow](https://airflow.apache.org/) - Orquestração de pipelines de dados
- [DBT (Data Build Tool)](https://www.getdbt.com/) - Transformação e modelagem de dados
- [Apache Superset](https://superset.apache.org/) - Visualização e exploração de dados
- [PostgreSQL](https://www.postgresql.org/) - Banco de dados relacional
- [Docker](https://www.docker.com/) - Containerização e implantação de aplicações

## Primeiros passo

###  Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados:

- **Docker e Docker Compose**: Para gerenciamento de contêineres.
- **Make**: Ferramenta de automação de build.
- **Python 3.x**: Para execução de scripts e desenvolvimento.
- **Git**: Controle de versão.

Caso precise de ajuda para instalar esses componentes, consulte a documentação oficial de cada ferramenta:

- [Instalação do Docker](https://docs.docker.com/get-docker/)
- [Guia do Python](https://www.python.org/downloads/)
- [Guia do Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

---

## 🚀 Instalação

### 1. Clonando o Repositório

Para obter o código-fonte do projeto, clone o repositório Git:

```bash
git clone git@gitlab.com:lappis-unb/gest-odadosipea/app-lappis-ipea.git
cd app-lappis-ipea
```

### 2. Configurando o Ambiente

Execute o comando abaixo para configurar automaticamente o ambiente de desenvolvimento:

```bash
make setup
```

Este comando irá:

- Criar ambientes virtuais necessários.
- Instalar dependências do projeto.
- Configurar hooks de pré-commit.
- Preparar o ambiente de desenvolvimento para execução local.

!!! note "Dica" Caso encontre problemas durante a configuração, verifique se o Docker está rodando corretamente e se você possui permissões administrativas no sistema.

## 🏃‍♂️ Executando o Projeto Localmente

Após a configuração, inicialize todos os serviços com o Docker Compose:

```bash
docker-compose up -d
```

### Acessando os Componentes

Uma vez que os serviços estejam em execução, você pode acessar as ferramentas principais nos seguintes URLs:

- Airflow: http://localhost:8080
- Jupyter: http://localhost:8888
- Superset: http://localhost:8088

Certifique-se de que todas as portas mencionadas estejam disponíveis no seu ambiente.

## 🛠 Estrutura do Projeto

A estrutura do projeto é organizada para separar cada componente da stack, facilitando a manutenção e o desenvolvimento:

```bash
.
├── airflow/           # Configurações e DAGs do Airflow
│   ├── dags/          # Definição de workflows
│   └── plugins/       # Plugins personalizados
├── dbt/               # Modelos e configurações do dbt
│   └── models/        # Modelagem de dados
├── jupyter/           # Notebooks interativos
│   └── notebooks/     # Análises exploratórias
├── superset/          # Dashboards e visualizações
│   └── dashboards/    # Configurações de dashboards
├── docker-compose.yml # Configuração do Docker Compose
├── Makefile           # Comandos automatizados
└── README.md          # Documentação inicial
```

Essa organização modular permite que cada componente seja desenvolvido e mantido de forma independente.

---

## 🎯 Comandos Úteis no Makefile

O **Makefile** facilita a execução de tarefas repetitivas e a configuração do ambiente. Aqui estão os principais comandos disponíveis:

- `make setup`: Configuração inicial do projeto, incluindo instalação de dependências e configuração do ambiente.
- `make lint`: Verificação de qualidade do código com ferramentas de linting.
- `make tests`: Execução da suíte de testes para validar mudanças no código.
- `make clean`: Remoção de arquivos gerados automaticamente.
- `make build`: Criação de imagens Docker para o ambiente de desenvolvimento.


## Equipe

Gov Hub BR - transformando dados públicos em ativos estratégicos.
