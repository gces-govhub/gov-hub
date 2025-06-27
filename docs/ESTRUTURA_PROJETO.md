# Gov-Hub - Estrutura Organizada do Projeto

## 📁 Estrutura de Diretórios

```
gov-hub/
├── .github/                 # Templates e configurações do GitHub
│   └── pull-request-template.md
├── config/                  # Arquivos de configuração
│   ├── config.json         # Configuração principal do sistema
│   └── giscus.json         # Configuração do sistema de comentários
├── data/                    # Dados do projeto
│   ├── processed/          # Dados processados
│   └── raw/               # Dados brutos baixados
├── docs/                    # Documentação completa
│   ├── guias/              # Guias técnicos
│   ├── poc/                # Documentação da POC
│   ├── relatorios/         # Relatórios de execução
│   ├── INDICE_DOCUMENTACAO.md
│   └── README_FINAL.md
├── legacy/                  # Scripts originais (backup)
├── logs/                    # Arquivos de log
├── notebooks/               # Jupyter notebooks para análise
├── requirements/            # Arquivos de dependências
│   ├── requirements-dev.txt
│   └── requirements_simple.txt
├── scripts/                 # Scripts de automação
│   ├── run_final_refactored.ps1
│   ├── setup_final.ps1
│   ├── validate_final_refactored.ps1
│   └── run_poc.sh
├── src/                     # Código fonte principal
│   └── govhub/             # Pacote Python principal
│       ├── core/           # Módulos principais
│       └── utils/          # Utilitários
├── tests/                   # Testes unitários
└── tools/                   # Ferramentas auxiliares
```

## 📋 Arquivos Principais na Raiz

Mantidos na raiz apenas os arquivos essenciais do projeto:

- `README.md` - Documentação principal
- `pyproject.toml` - Configuração do projeto Python
- `requirements.txt` - Dependências principais
- `package.json` - Configuração Node.js/TypeScript
- `mkdocs.yml` - Configuração da documentação
- `Dockerfile` - Containerização
- `LICENSE` - Licença do projeto
- `.gitignore` - Arquivos ignorados pelo Git

## 🔧 Principais Mudanças

### Arquivos Movidos:

1. **Configurações** → `config/`
   - `config.json` → `config/config.json`
   - `giscus.json` → `config/giscus.json`

2. **Documentação** → `docs/`
   - Relatórios → `docs/relatorios/`
   - Guias → `docs/guias/`
   - POC → `docs/poc/`

3. **Logs** → `logs/`
   - `govhub_data_acquisition.log`
   - `validation_report.txt`

4. **Scripts** → `scripts/`
   - `run_poc.sh`

5. **Dependências** → `requirements/`
   - `requirements-dev.txt`
   - `requirements_simple.txt`

### Imports Atualizados:

- Todas as referências a `config.json` → `config/config.json`
- Scripts de validação atualizados para nova estrutura
- Paths relativos corrigidos nos módulos Python

## ✅ Validação

Execute para validar a nova estrutura:

```powershell
cd scripts
.\validate_final_refactored.ps1
```

Execute para testar o pipeline completo:

```powershell
cd scripts
.\run_final_refactored.ps1
```

## 📈 Benefícios da Reorganização

1. **Organização Clara**: Cada tipo de arquivo em sua pasta específica
2. **Escalabilidade**: Estrutura preparada para crescimento do projeto
3. **Manutenibilidade**: Fácil localização e manutenção de arquivos
4. **Profissionalismo**: Estrutura padrão da indústria
5. **Colaboração**: Estrutura familiar para novos desenvolvedores

---

*Estrutura atualizada em: 26 de junho de 2025*
