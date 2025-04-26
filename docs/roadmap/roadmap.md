# 🚀 Implementação de Agente de IA para Extração Automática de Identificadores

## 🎯 Objetivo

Expandir o pipeline de dados do GovHubbr com a integração de um Agente de IA responsável pela extração automática de identificadores em campos de observação textual nas bases de dados públicas.

Exemplos de identificadores extraídos:
- num_transf
- contrato_num
- contrato_licitacao
- instrumento_numero
- nc_aux
- nc_prefix
- nc_posfix
- nc


Esta funcionalidade é crítica para aprimorar a integração de bases de dados, automatizar o cruzamento de informações e fortalecer a qualidade das análises realizadas.

---

## 📦 Dependências Técnicas

- **Python 3.10+:** Ambiente de desenvolvimento principal.
- **HuggingFace Transformers:**
    - Modelo: BERTimbau Base para NER.
    - Task: Token-Classification para extrair entidades como NF, Contrato, Processo.
- **pandas**: Manipulação de datasets tabulares.
- **Apache Airflow**: Orquestração do pipeline de execução.
- **DBT**: Transformações intermediárias no pipeline de dados.
- **PostgreSQL**: Armazenamento dos dados extraídos.

### Dependências Adicionais para PoC
- OpenAI API ou Alternativa Open Source (por exemplo, HuggingFace Inference API).
- Jupyter Notebook: Ambiente de prototipação rápida para extração de informações.
- Transformers (HuggingFace): Para testes com modelos públicos de extração textual.
- openai Python SDK (se usar OpenAI).

---

## 🧪 Fase de Teste de Conceito e Avaliação de Estratégias de Extração
Antes da implementação definitiva do Agente de IA no pipeline de produção, será realizada uma Fase de Teste de Conceito (PoC) para:
- Avaliar a viabilidade da extração automática de identificadores em campos de texto livres.
- Testar rapidamente diferentes estratégias de NLP utilizando APIs já disponíveis.
- Identificar desafios e limitações práticas na interpretação dos textos de observação.

### Estratégia do Teste:
1. Ambiente:
    - Rodar os experimentos iniciais em Jupyter Notebooks.
    - Utilizar amostras reais dos campos observacao da Tabela B.

2. Ferramentas:
    - GPT-3.5-turbo via OpenAI API para tarefas de extração textual supervisionada.
    - Alternativas Open Source via HuggingFace, caso necessário.

3. Metodologia:
    - Inserir exemplos reais de campos de observação.
    - Formular prompts para extrair explicitamente os identificadores desejados.

4. Avaliar:
    - Se o modelo consegue extrair corretamente os campos (num_transf, contrato_num, etc).
    - Se há confusão ou ambiguidade.
    - Tempo de inferência, custo e viabilidade prática.

5. Critérios de Sucesso:
    - Precisão acima de 85% na extração dos identificadores relevantes em pelo menos 80% dos casos testados.
    - Custo computacional e de API dentro dos limites viáveis para posterior migração para BERTimbau.


## 🛠️ Arquitetura de Integração da Funcionalidade

1. **Input (Bronze):**
    - Tabela A: (num_transf, contrato_num, etc).
    - Tabela B: (observacao).
2. Execução da Extração:
    - Durante a transformação no DBT, um script externo Python (chamado via macro ou dbt-python-model) é invocado.
    - O agente de IA processa o campo observacao da Tabela B e extrai os identificadores.
3. Matching e Merge:
    - Após a extração, realiza-se o JOIN entre:
        - Identificadores extraídos da Tabela B
        - Identificadores originais da Tabela A
    - Match feito usando lógica de tolerância a erro mínima (fuzzy matching controlado se necessário).
4. Output (Silver):
    - Nova Tabela Silver consolidando:
        - Dados estruturados da Tabela A
        - Informações adicionais da Tabela B

Esse processamento ocorrerá **dentro do fluxo ETL** já existente, entre a transformação DBT e o carregamento final no PostgreSQL.

---

# 📆 Planejamento por Releases (Funcionalidade)

## 📍 Release I — Infraestrutura e Preparação (28/04/2025)

**Objetivos:**
- Instalar e configurar dependências (spaCy, regex, pandas).
- Estruturar ambiente de desenvolvimento da funcionalidade.
- Estudo inicial dos padrões de texto dos campos de observação.
- Definição do escopo dos identificadores a serem extraídos.

**Entregas:**
- Ambiente Docker configurado para NLP.
- Documento técnico: "Padrões de Texto e Estratégias de Extração".
- Criação do branch `feature/ai-extraction-preparation`.

---

## 📍 Release II — Teste de Conceito (PoC) e Avaliação (02/06/2025)

**Objetivos:**
- Desenvolver protótipos de extração utilizando modelos de linguagem via HuggingFace Transformers.
- Implementar teste de conceito alternativo utilizando OpenAI API (ou outro modelo gratuito) em ambiente Jupyter Notebook.
- Avaliar o desempenho das abordagens quanto à extração correta dos identificadores.
- Definir a solução técnica a ser implementada no pipeline definitivo.

**Entregas:**
- Branch `feature/ai-extraction-poc` criado e publicado.
- Scripts de extração com BERTimbau documentados e versionados.
- Relatório técnico de avaliação comparativa de abordagens.

---

## 📍 Release III — Implementação Final e Integração (25/06/2025)

**Objetivos:**
- Implementar o agente de IA definitivo baseado na solução aprovada (HuggingFace + BERTimbau).
- Integrar o agente de extração ao pipeline de dados DBT.
- Realizar o processo de matching e merge entre as Tabelas A e B, consolidando a nova Tabela Silver
- Automatizar a execução do processo dentro do Airflow.
- Produzir documentação detalhada para operação e manutenção da funcionalidade.

**Entregas:**
- Branch `feature/ai-extraction-final` criada e mergeada.
- Pipeline DBT atualizado com execução da extração e integração dos dados.
- Nova Tabela Silver consolidada disponível em PostgreSQL.
- Documentação da funcionalidade publicada.



# 🎡 Épicos, Features e Histórias de Usuário

## Épico 1: Preparação e Ambiente
- Configuração de ambiente Docker.
- Estudo exploratório dos campos de observação.

## Épico 2: Teste de Conceito
- Desenvolvimento de protótipos utilizando APIs e Transformers.
- Avaliação de performance e viabilidade.

## Épico 3: Desenvolvimento e Deploy Final
- Desenvolvimento do agente definitivo.
- Integração ao pipeline DBT e Airflow.
- Deploy final e disponibilização da nova Tabela Silver.

---

## 🛠️ Features (Principais Funcionalidades)
Criação de ambiente padronizado para processamento NLP.

Desenvolvimento do agente de extração com HuggingFace Transformers.

Integração da extração automática na transformação DBT.

Implementação do processo de matching automatizado para construção da Tabela Silver.


## 📋 Histórias de Usuário

- **Usuário 1**: Como analista de dados, quero extrair automaticamente identificadores a partir de descrições textuais, para permitir integrações precisas entre bases.
- **Usuário 2**: Como cientista de dados, quero validar abordagens de extração utilizando diferentes modelos de NLP para garantir a maior precisão possível na correspondência dos identificadores.
- **Usuário 3**: Como gestor público, quero acessar dashboards e relatórios que consolidem informações de forma automatizada e confiável, facilitando a tomada de decisão.

---