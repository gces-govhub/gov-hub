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

