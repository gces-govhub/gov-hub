# Dicionário de Dados - Gov Hub BR

## 1. Plugins

### 1.1 Blog

#### Schema: `docs/schema/plugins/blog.json`

- **Campos principais:**
  - `title` (string): Título do post do blog.
  - `author` (string): Nome do autor.
  - `date` (string): Data de publicação.
  - `tags` (array de string): Lista de tags associadas ao post.
  - `summary` (string): Resumo do post.
  - `content` (string): Conteúdo em Markdown.
  - `readtime` (integer): Tempo estimado de leitura (em minutos).

#### Estrutura de dados (exemplo):

| Campo     | Tipo    | Descrição                        | Exemplo                |
|-----------|---------|----------------------------------|------------------------|
| title     | string  | Título do post                   | "Como contribuir"      |
| author    | string  | Nome do autor                    | "João Silva"           |
| date      | string  | Data de publicação               | "2025-05-16"           |
| tags      | array   | Tags associadas                  | ["contribuição", "dev"]|
| summary   | string  | Resumo do post                   | "Guia para contribuir" |
| content   | string  | Conteúdo em Markdown             | "# Como contribuir..." |
| readtime  | int     | Tempo de leitura estimado (min)  | 4                      |

---

### 1.2 Group

#### Schema: `docs/schema/plugins/group.json`

- **Campos principais:**
  - `name` (string): Nome do grupo.
  - `description` (string): Descrição do grupo.
  - `members` (array de string): Lista de membros do grupo.

| Campo       | Tipo    | Descrição                        | Exemplo           |
|-------------|---------|----------------------------------|-------------------|
| name        | string  | Nome do grupo                    | "Equipe Dev"      |
| description | string  | Descrição do grupo               | "Time de backend" |
| members     | array   | Lista de membros                 | ["João", "Maria"] |

---

### 1.3 Info

#### Schema: `docs/schema/plugins/info.json`

- **Campos principais:**
  - `project` (string): Nome do projeto.
  - `version` (string): Versão atual.
  - `maintainers` (array de string): Responsáveis pelo projeto.
  - `contact` (string): E-mail de contato.

| Campo       | Tipo    | Descrição                        | Exemplo           |
|-------------|---------|----------------------------------|-------------------|
| project     | string  | Nome do projeto                  | "Gov Hub BR"      |
| version     | string  | Versão do projeto                | "0.1.0"           |
| maintainers | array   | Responsáveis                     | ["João", "Maria"] |
| contact     | string  | E-mail de contato                | "contato@ex.com"  |

---

## 2. Plugins Externos (schemas em `docs/schema/plugins/external/`)

- **gen-files.json:** Geração de arquivos.
- **git-authors.json:** Autores do repositório.
- **git-committers.json:** Committers do repositório.
- **git-revision-date.json:** Datas de revisão dos arquivos.
- **literate-nav.json:** Navegação literária.
- **macros.json:** Macros de configuração.
- **minify.json:** Configuração de minificação.
- **redirects.json:** Redirecionamentos de páginas.
- **section-index.json:** Índice de seções.

Cada schema define campos específicos para configuração e integração de funcionalidades na documentação e no site.

---

## 3. Observações

- Os dados acima são estruturados em arquivos JSON e consumidos pelos plugins Python localizados em `src/plugins/`.
- Para detalhes sobre cada campo, consulte os arquivos JSON em `docs/schema/plugins/` e os scripts Python correspondentes em `src/plugins/`.
- O dicionário deve ser atualizado sempre que houver mudanças nos schemas ou nos plugins.

---