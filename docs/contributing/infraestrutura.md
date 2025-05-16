# Infraestrutura do Projeto

Este documento descreve a infraestrutura técnica da plataforma Gov Hub, com o objetivo de orientar a comunidade, novos contribuidores e equipes técnicas sobre o funcionamento, manutenção e boas práticas adotadas. A plataforma está estruturada com foco em **ambientes separados**, **entrega contínua** e **alta disponibilidade**.

## Visão Geral

A infraestrutura é baseada em dois clusters Kubernetes:

- **Cluster de Homologação**: mantido pelo LAPPIS, utilizado para testes e validações.
- **Cluster de Produção**: mantido pelo IPEA, onde o ambiente estável é disponibilizado ao público.

Utilizamos o **[Rancher](https://www.rancher.com/)** para gerenciar os clusters, e o **[ArgoCD](https://argo-cd.readthedocs.io/en/latest/)** para entrega contínua e sincronização entre os ambientes, adotando a arquitetura de **App of Apps**.

---

## Estrutura dos Ambientes

### 🔧 Cluster de Homologação

- Gerenciado pela equipe do LAPPIS.
- Ambiente mais flexível, com controle total sobre permissões.
- App of Apps configurado para suportar múltiplos ambientes via **overlays** (homologação e produção).
- Utilizado para testes antes da publicação em produção.

### 🚀 Cluster de Produção

- Hospedado na infraestrutura do IPEA.
- Requer processo específico de obtenção de acesso para instalação de CRDs do ArgoCD.
- ArgoCD foi instalado e configurado com suporte à alta disponibilidade (exceto Redis, provisoriamente).
- Documentação de setup disponível [neste repositório GitLab](https://gitlab.com/lappis-unb/gest-odadosipea/infra-lappis-ipea/-/tree/main/argocd).

---

## Entrega Contínua (CD)

- Utilizamos o **ArgoCD** para sincronizar o estado dos clusters com os manifests versionados em repositórios Git (GitOps).
- A maioria das aplicações utiliza imagens de containers públicas.
- Para aplicações como o **Airflow**, que exigem dependências específicas:
  - Um passo adicional foi incluído no pipeline de CI para gerar e publicar imagens customizadas com base no `Dockerfile` e `requirements.txt`.
  - A publicação da imagem é feita manualmente pelo desenvolvedor responsável por atualizações — garantindo controle e responsabilidade.

---

## Boas Práticas e Alta Disponibilidade

- O cluster de homologação já estava bem configurado para lidar com instabilidades (por ser ambiente de teste).
- O cluster de produção está sendo revisado continuamente para garantir:
  - Alta disponibilidade das aplicações.
  - ArgoCD em modo HA (High Availability).
  - Monitoramento de serviços e alertas.
- O **Redis** ainda não está em HA por limitação de recursos, mas será ajustado assim que novas máquinas forem provisionadas.

---

## Contribuindo com a Infraestrutura

Se você deseja contribuir com melhorias na infraestrutura:

1. Verifique a documentação do ArgoCD e Rancher utilizada neste projeto.
2. Siga os padrões de overlays definidos no App of Apps.
3. Realize testes primeiro no cluster de homologação.
4. Documente qualquer mudança de configuração no repositório de infraestrutura.

Para dúvidas ou sugestões, entre em contato com a equipe via [issues](https://github.com/gces-govhub/gov-hub/issues) ou participe das discussões no canal da comunidade.

---

**Manutenção:** Equipe Gov Hub – LAPPIS/UnB & IPEA  
**Última atualização:**  16/05/2025
