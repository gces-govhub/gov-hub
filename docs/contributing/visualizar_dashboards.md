# 📊 Guia de Visualização de Dados com Apache Superset

## Como vizualizar dashbords usando apache superset

Este guia tem como objetivo orientar o uso do **Apache Superset** para conectar um banco de dados PostgreSQL, registrar datasets e criar dashboards interativos de forma simples.

---

## 1. Conectando o Superset ao banco de dados PostgreSQL

1. Acesse o Superset no navegador.
2. No canto superior direito, clique no botão **`+`** e selecione **`Data` → `Connect Database`**.
3. Escolha o tipo de banco de dados (**PostgreSQL**).
4. Preencha os dados de conexão. Você pode usar a URI SQLAlchemy:

    ```bash
    postgresql://usuario:senha@host:porta/nome_do_banco
    ```

    > 💡 Dica: Se estiver usando Docker, o host pode ser `host.docker.internal`.

5. Clique em **`Test Connection`** para verificar a conexão.
6. Se tudo estiver correto, clique em **`Connect`** para salvar.

---

## 2. Registrando um Dataset (Tabela)

1. Vá até **`Data` → `Datasets`**.  
2. Clique no botão **`+ Dataset`** no canto superior direito.  
3. Na janela que abrir:

    - Escolha o banco de dados conectado.
    - Selecione o **Schema**.
    - Escolha a **Tabela** que deseja analisar.

4. Clique em **`Add`** para registrar o dataset.

---

## 3. Personalizando as colunas (opcional)

1. Após adicionar um dataset, clique nele na lista.
2. Clique em **`Edit Dataset`** (ícone de lápis).
3. Para cada coluna, você pode:

    - Marcar se é temporal (datas/horários).
    - Definir como filtrável.
    - Adicionar descrições ou expressões personalizadas.
    - Criar **métricas virtuais** (ex: `SUM(receita`).
    - Criar **colunas calculadas** (ex: `CAST(valor AS FLOAT)`).

---

## 4. Criando gráficos (charts)

1. No menu **Datasets**, clique no nome do dataset que deseja visualizar.  
2. Isso abrirá o modo **Explore**, onde você pode criar gráficos com interface no-code.  
3. Na tela de Explore:

    - Selecione o tipo de visualização (ex: Bar Chart, Time Series, Pie, etc).
    - Defina a métrica (ex: soma de vendas).
    - Escolha dimensões e filtros (ex: por região, por produto).

4. Clique em **`Run`** para visualizar o gráfico.  
5. Quando estiver satisfeito, clique em **`Save`**:

    - Dê um nome ao gráfico.
    - Escolha adicionar a um dashboard existente ou criar um novo.

---

## 5. Criando e organizando um Dashboard

1. Após salvar o gráfico, selecione **`Save and go to Dashboard`**.  
2. No dashboard, clique em **`Edit Dashboard`** (canto superior direito).  
3. Agora é possível:

    - Redimensionar os gráficos (arrastar as bordas).
    - Mover os gráficos pela grade.
    - Adicionar outros charts, markdowns e filtros.

4. Clique em **`Save`** para salvar o layout do dashboard.

---

## 6. Gerenciando acesso a dashboards

- **Proprietários**: têm permissão para editar.
- **Usuários não-proprietários**: acesso pode ser gerenciado de duas formas:
- **Permissões por dataset**: se o usuário tiver acesso ao dataset, também pode ver os dashboards que o usam.
- **Dashboard Roles (RBAC)**: se ativado, você pode definir quem vê o dashboard, independentemente do dataset.

---

## 7. Customizando a visualização do dashboard via URL

Você pode adicionar parâmetros à URL para alterar como o dashboard é exibido:

| Parâmetro | Opções         | Descrição |
|----------|----------------|-----------|
| `standalone` | 0 (default), 1, 2, 3 | Remove elementos da interface (ex: navegação, título) |
| `show_filters` | 0, 1 (default) | Oculta ou exibe a barra de filtros |
| `expand_filters` | 0, 1 | Controla se a barra de filtros aparece expandida |

Exemplo de URL:

```bash
http://localhost:8088/superset/dashboard/my-dashboard/?standalone=1&show_filters=0
```
