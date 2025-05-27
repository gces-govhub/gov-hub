# Guia de Usuário - Gov Hub BR

Bem-vindo ao Gov Hub BR! Este guia irá ajudá-lo a acessar, navegar e utilizar as principais funcionalidades da plataforma.

---

## 1. Acesso à Plataforma

- **Ambiente Local:**  
  Após rodar `docker-compose up -d`, acesse os serviços nos seguintes endereços:
  - Airflow: [http://localhost:8080](http://localhost:8080)
  - Jupyter: [http://localhost:8888](http://localhost:8888)
  - Superset: [http://localhost:8088](http://localhost:8088)

- **Ambiente de Produção:**  
  O endereço será fornecido pela equipe de TI ou estará disponível na documentação interna.

---

## 2. Autenticação

- **Primeiro acesso:**  
  Use as credenciais fornecidas pelo administrador.
- **Recuperação de senha:**  
  Siga o fluxo de “Esqueci minha senha” (se disponível) ou solicite suporte.

---

## 3. Funcionalidades Principais

### 3.1. Visualização de Dashboards (Superset)

1. Acesse o Superset.
2. No menu lateral, clique em “Dashboards”.
3. Selecione o dashboard desejado para visualizar gráficos e tabelas.
4. Use filtros para refinar os dados exibidos.
5. Para exportar dados, clique no ícone de download disponível em cada gráfico.

### 3.2. Execução de Pipelines (Airflow)

1. Acesse o Airflow.
2. Veja a lista de DAGs (workflows).
3. Para rodar um pipeline, clique no botão de play ao lado do nome do DAG.
4. Acompanhe o status da execução em tempo real.
5. Para ver logs, clique no DAG e depois em “Log”.

### 3.3. Análise Exploratória (Jupyter)

1. Acesse o Jupyter.
2. Clique em “notebooks” para ver os arquivos disponíveis.
3. Abra um notebook para explorar dados ou criar análises.
4. Execute células de código com Shift+Enter.

---

## 4. Dúvidas Frequentes

- **Serviço não abre:**  
  Verifique se o Docker está rodando e se as portas não estão ocupadas.
- **Erro de permissão:**  
  Execute o terminal como administrador ou peça suporte.
- **Exportação de dados:**  
  Use a opção de download nos dashboards do Superset.

---

## 5. Suporte

- Para dúvidas técnicas, abra uma issue no repositório ou entre em contato pelo canal oficial do projeto.

---
