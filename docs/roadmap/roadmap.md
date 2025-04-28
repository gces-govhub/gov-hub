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
    - OpenAI API para tarefas de extração textual supervisionada.
    - Alternativas Open Source, caso necessário.

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
    - Match feito usando lógica de tolerância a erro mínima.
4. Output (Silver):
    - Nova Tabela Silver consolidando:
        - Dados estruturados da Tabela A
        - Informações adicionais da Tabela B

Esse processamento ocorrerá **dentro do fluxo ETL** já existente, entre a transformação DBT e o carregamento final no PostgreSQL.

---

# 📆 Planejamento por Versões

## 📍 Versão 1.0.0 — Estruturação Inicial e Ambientação

**Objetivos:**

- Aprimorar a documentação do projeto e seus componentes.
- Realizar estudo preliminar sobre a viabilidade de extração automática de identificadores.
- Revisar e organizar o ambiente de desenvolvimento para futuras implementações.
- Definir os primeiros requisitos técnicos para o Teste de Conceito (PoC).


**Entregas:**

- Atualização e melhoria das documentações MkDocs existentes.
- Planejamento do escopo do Teste de Conceito (PoC).

---

## 📍 Versão 1.1.0 — Teste de Conceito de Extração de Identificadores

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

## 📍 Versão 2.0.0 — Implementação do Agente Definitivo e Integração no Pipeline

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

## 📚 Épico 1: Organização e Preparação Inicial
> Preparação do ambiente, documentação e análise preliminar.

- **Feature 1.1: Atualizar a documentação técnica do projeto**
    - (Sem história de usuário direta)

- **Feature 1.2: Estudo dos padrões de observação**
    - **História de Usuário 1**:  
      _Como cientista de dados, quero entender os padrões dos campos de observação para planejar a melhor abordagem de extração._

- **Feature 1.3: Definição do planejamento do PoC**
    - **História de Usuário 2**:  
      _Como analista de dados, quero definir previamente as estratégias de extração para guiar o desenvolvimento do Teste de Conceito._

---

## 📚 Épico 2: Teste de Conceito para Extração de Identificadores
> Prototipagem, teste e avaliação de abordagens de IA para extração.

- **Feature 2.1: Desenvolvimento de protótipo usando OpenAI API**
    - **História de Usuário 3**:  
      _Como cientista de dados, quero testar a extração de identificadores usando modelos de linguagem prontos para validar viabilidade rápida._

- **Feature 2.2: Desenvolvimento de protótipo usando HuggingFace Transformers**
    - **História de Usuário 4**:  
      _Como cientista de dados, quero desenvolver um protótipo open-source para garantir independência tecnológica e redução de custos._

- **Feature 2.3: Avaliação e comparação das abordagens**
    - **História de Usuário 5**:  
      _Como analista de dados, quero comparar o desempenho dos modelos para escolher a melhor abordagem para produção._

- **Feature 2.4: Documento de decisão técnica**
    - (Sem história de usuário direta.)

---

## 📚 Épico 3: Desenvolvimento e Integração do Agente Definitivo
> Construção e implantação do agente final no pipeline de produção.

- **Feature 3.1: Implementar agente HuggingFace Transformers definitivo**
    - **História de Usuário 6**:  
      _Como analista de dados, quero contar com um agente de extração treinado e validado para automatizar o processamento dos dados._

- **Feature 3.2: Integração no pipeline DBT**
    - **História de Usuário 7**:  
      _Como engenheiro de dados, quero integrar a extração no DBT para padronizar a transformação dos dados sem processos manuais._

- **Feature 3.3: Implementar lógica de matching e merge entre tabelas**
    - **História de Usuário 8**:  
      _Como analista de dados, quero garantir o cruzamento correto de dados entre tabelas para consolidar informações de forma automatizada._

- **Feature 3.4: Automatizar execução no Airflow**
    - **História de Usuário 9**:  
      _Como engenheiro DevOps, quero automatizar a orquestração da extração para manter o pipeline escalável e confiável._

- **Feature 3.5: Atualizar a Tabela Silver consolidada**
    - **História de Usuário 10**:  
      _Como gestor público, quero acessar dashboards e relatórios baseados em dados consolidados para facilitar auditorias e decisões._

---
