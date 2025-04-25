name: "Proposta de Conteúdo ou Funcionalidade"
description: "Use este template para propor novos conteúdos, como um guia ou página, ou sugerir novas funcionalidades."
title: "[ideia] <título da proposta>"
labels: ["conteúdo", "ideia"]
body:
  - type: markdown
    attributes:
      value: |
        Antes de abrir esta issue, verifique se já existe uma issue semelhante [nesta lista](https://github.com/GovHub-br/gov-hub/issues) para evitar duplicações.

  - type: textarea
    id: proposta
    attributes:
      label: "Descreva sua proposta"
      description: |
        - Explique claramente o que você está propondo.
        - Por que essa proposta é importante?
        - Como ela contribui para o projeto como um todo?
        - Se possível, indique um caminho ou solução para a proposta.
    validations:
      required: true

  - type: textarea
    id: localizacao
    attributes:
      label: "Onde esse conteúdo ou funcionalidade deve ser incluído?"
      description: "Se aplicável, indique páginas ou seções relacionadas onde esse conteúdo pode ser adicionado."
    validations:
      required: false

  - type: checkboxes
    id: tarefas
    attributes:
      label: "Tarefas a serem realizadas"
      options:
        - label: "Este item é uma das tarefas a serem realizadas."
    validations:
      required: false

  - type: checkboxes
    id: validacao
    attributes:
      label: "Checklist de validação (Deve ser preenchido por um revisor)"
      options:
        - label: "Este item é um requisito para o fechamento da issue."
    validations:
      required: false
