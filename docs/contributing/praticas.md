# Melhores práticas do repositório

Para garantir a manutenção da qualidade, organização e escalabilidade deste repositório, é fundamental seguir as melhores práticas descritas a seguir. Elas foram definidas com base em padrões consolidados da engenharia de software e visam facilitar a colaboração, revisão de código e evolução contínua do projeto.

## 📌 Abertura de Issues

Toda solicitação de mudança, correção de bug ou sugestão de melhoria deve ser registrada por meio de uma *issue*. As *issues* devem ser abertas utilizando o modelo padrão fornecido pelo repositório, o qual ajuda a manter a clareza, rastreabilidade e organização da discussão. Certifique-se de preencher todos os campos obrigatórios com informações precisas, como contexto, impacto e possíveis caminhos de solução.

## 🧱 Arquitetura e Modelagem de Dados

A modelagem de dados e a organização dos esquemas devem seguir a arquitetura em camadas definida para o repositório, baseada nos estágios de maturidade e tratamento dos dados. Esta abordagem facilita a rastreabilidade, o controle de qualidade e a evolução gradual dos dados ao longo do tempo. As camadas estão estruturadas da seguinte forma:

- **Raw**: camada bruta, que armazena os dados exatamente como foram recebidos da fonte, sem qualquer transformação. Serve como fonte de verdade e histórico imutável.
- **Bronze**: camada de dados limpos e estruturados de forma padronizada, com correções mínimas (como tipos de dados e normalização básica), mantendo a granularidade original.
- **Silver**: camada onde os dados passam por enriquecimentos, junções e integrações entre diferentes fontes, além de validações mais complexas.
- **Gold**: camada final, otimizada para consumo e análise. Contém métricas, agregações e tabelas derivadas voltadas a casos de uso específicos, como dashboards, relatórios e serviços.

Ao propor modificações ou novos pipelines, certifique-se de posicionar corretamente os dados dentro dessa estrutura e seguir os padrões de nomenclatura, versionamento e particionamento definidos. Alterações em qualquer uma dessas camadas devem ser devidamente documentadas e revisadas pelo time responsável, garantindo consistência e rastreabilidade.

Essa organização em camadas é fundamental para garantir qualidade, confiabilidade e governança sobre os dados tratados no repositório.

## 🔄 Pull Requests

Todas as contribuições de código devem ser feitas através de *Pull Requests (PRs)*. Utilize o modelo de PR disponibilizado no repositório para garantir que informações essenciais — como escopo da mudança, contexto e validação — estejam claras e organizadas. PRs devem ser pequenas, focadas e atômicas sempre que possível, facilitando a revisão e evitando regressões.

Além disso, todo PR deve ser revisado por pelo menos um outro membro do time antes de ser mesclado na branch principal. Discussões e sugestões durante o processo de *code review* são altamente encorajadas, com foco na melhoria contínua da base de código.

## 📝 Commits

As mensagens de commit devem seguir um padrão pré-definido, inspirado no *Conventional Commits*, com prefixos como:

- `feat:` para novas funcionalidades;
- `fix:` para correções de bugs;
- `docs:` para alterações na documentação;
- `ci:` para mudanças relacionadas a integração contínua;
- `refactor:` para melhorias no código que não alteram comportamento.

Cada mensagem de commit deve conter uma descrição clara, objetiva e sucinta da mudança implementada. Quando necessário, utilize a descrição estendida do commit para detalhar motivações, impactos e decisões técnicas importantes. Isso facilita o entendimento histórico das mudanças e contribui para uma base de código mais sustentável e auditável.

---

## 🤝 Convivência, respeito e ética na colaboração

A colaboração neste repositório deve sempre ocorrer em um ambiente de respeito mútuo, empatia e abertura ao diálogo. Espera-se que todas as interações — sejam em issues, pull requests, revisões de código ou discussões técnicas — sejam conduzidas com educação, cordialidade e espírito colaborativo. Críticas devem ser construtivas, com foco na solução e na melhoria contínua, nunca direcionadas de forma pessoal.

**Não será tolerado nenhum tipo de discurso ou comportamento ofensivo**, discriminatório, agressivo ou de ódio. Isso inclui, mas não se limita a: racismo, sexismo, homofobia, xenofobia ou qualquer outra forma de preconceito. A manutenção de um ambiente saudável, inclusivo e profissional é responsabilidade de todos os colaboradores e condição essencial para a participação neste projeto.

Contribuir com respeito é tão importante quanto contribuir com código.
