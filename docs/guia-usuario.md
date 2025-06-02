# Guia de Usuário - GovHubBR

Seja bem-vindo ao **GovHubBR**! Este guia tem como objetivo orientá-lo no acesso, navegação e utilização das principais funcionalidades da plataforma.

---

## 🔓 1. Acesso à Plataforma

### Ambiente Local

Após executar o comando abaixo:

```bash
docker-compose up -d
```

Acesse os seguintes serviços em seu navegador:

- **Airflow**: [http://localhost:8080](http://localhost:8080)
- **Jupyter**: [http://localhost:8888](http://localhost:8888)
- **Superset**: [http://localhost:8088](http://localhost:8088)

### Ambiente de Produção

O endereço de produção será fornecido pela equipe de TI ou estará disponível na documentação interna da instituição.

---

## 🔐 2. Autenticação

- **Primeiro Acesso**: Utilize as credenciais fornecidas pelo administrador do sistema.
- **Recuperação de Senha**: Caso o sistema disponha da opção "Esqueci minha senha", siga o fluxo indicado. Se não estiver disponível, entre em contato com o suporte.

---

## 📊 3. Funcionalidades Principais

### 3.1. Visualização de Dashboards (Superset)

1. Acesse o Superset.
2. No menu lateral, clique em **"Dashboards"**.
3. Selecione o dashboard desejado.
4. Utilize os filtros para refinar os dados.
5. Para exportar dados, clique no ícone de download presente em cada gráfico.

### 3.2. Execução de Pipelines (Airflow)

1. Acesse o Airflow.
2. Visualize a lista de **DAGs (workflows)**.
3. Para iniciar um pipeline, clique no ícone de **play** ao lado da DAG.
4. Acompanhe o status de execução em tempo real.
5. Clique no nome da DAG e em seguida em **"Log"** para visualizar os logs.

### 3.3. Análise Exploratória (Jupyter)

1. Acesse o Jupyter.
2. Navegue até a pasta **"notebooks"**.
3. Selecione e abra o notebook desejado.
4. Execute as células com `Shift + Enter`.

---

## ❓ 4. Dúvidas Frequentes

- **O serviço não abre:**
  - Verifique se o Docker está em execução e se as portas estão livres.

- **Erro de permissão:**
  - Tente abrir o terminal como administrador ou solicite suporte técnico.

- **Exportação de dados:**
  - Use o ícone de download nos gráficos dos dashboards do Superset.

---

## 📢 5. Suporte

Para dúvidas técnicas:

- Abra uma **issue** no repositório do projeto no GitHub.
- Ou entre em contato pelo **canal oficial de comunicação da equipe**.

---
