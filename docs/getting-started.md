# Getting Started with Data Pipeline Project

O **Data Pipeline Project** é uma solução moderna que utiliza ferramentas como **Airflow**, **DBT**, **Jupyter** e **Superset** para orquestração, transformação, análise e visualização de dados. Este guia ajudará você a começar rapidamente.

---

## 📋 Pré-requisitos

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

- Airflow: <http://localhost:8080>
- Jupyter: <http://localhost:8888>
- Superset: <http://localhost:8088>

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

## 🔐 Fluxo de Trabalho com Git

Este projeto utiliza **commits assinados digitalmente (GPG signing)** como parte do fluxo de trabalho. Siga os passos abaixo para configurar:

1. Gere uma chave GPG:

  ```bash
    gpg --full-generate-key
  ```

2. Configure o Git para usar sua chave GPG:

  ```bash
    git config --global user.signingkey YOUR_KEY_ID
    git config --global commit.gpgsign true
  ```

3. Adicione sua chave GPG à sua conta do GitLab:

   - Acesse as configurações da sua conta GitLab.
   - Cole a chave pública gerada pelo comando:

   ```bash
   gpg --armor --export YOUR_KEY_ID
   ```

Com isso, todos os seus commits estarão assinados e prontos para serem utilizados no projeto.

## 📚 Documentação Útil

Para aproveitar ao máximo os componentes do projeto, consulte as documentações oficiais:

- [Documentação do Airflow](https://airflow.apache.org/docs/)
- [Documentação do DBT](https://docs.getdbt.com/)
- [Documentação do Superset](https://superset.apache.org/docs/intro)
