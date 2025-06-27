# 🔐 Guia Definitivo para Configuração de Segredos - GitHub Actions

Este guia fornece instruções passo a passo para configurar todos os segredos necessários para o funcionamento completo dos pipelines de CI/CD do projeto Gov-Hub.

## 📋 Índice

1. [Segredos Necessários](#segredos-necessários)
2. [Como Acessar as Configurações de Segredos](#como-acessar-as-configurações-de-segredos)
3. [Configuração Passo a Passo](#configuração-passo-a-passo)
4. [Validação das Configurações](#validação-das-configurações)
5. [Troubleshooting](#troubleshooting)

---

## 🔑 Segredos Necessários

O projeto Gov-Hub requer os seguintes segredos para funcionamento completo:

### **Docker Hub (para builds e deploys de containers)**
- `DOCKER_USERNAME` - Nome de usuário do Docker Hub
- `DOCKERHUB_TOKEN` - Token de acesso do Docker Hub

### **AWS (para infraestrutura e deploy)**
- `AWS_REGION` - Região AWS (ex: `us-east-1`, `sa-east-1`)
- `AWS_ACCESS_KEY_ID` - Chave de acesso AWS
- `AWS_SECRET_ACCESS_KEY` - Chave secreta AWS

---

## 🛠️ Como Acessar as Configurações de Segredos

### **Passo 1: Navegue para o Repositório**
1. Acesse o repositório Gov-Hub no GitHub: `https://github.com/[SEU-USUARIO]/gov-hub`
2. Certifique-se de estar logado com uma conta que tenha permissões de administrador

### **Passo 2: Acesse as Configurações**
1. Clique na aba **"Settings"** (Configurações) no topo da página do repositório
2. No menu lateral esquerdo, procure pela seção **"Security"**
3. Clique em **"Secrets and variables"**
4. Selecione **"Actions"**

---

## ⚙️ Configuração Passo a Passo

### **🐳 Docker Hub - Configuração de Segredos**

#### **DOCKER_USERNAME**
1. Na página de segredos do GitHub Actions, clique em **"New repository secret"**
2. **Name:** `DOCKER_USERNAME`
3. **Secret:** Seu nome de usuário do Docker Hub (ex: `meunome`)
4. Clique em **"Add secret"**

#### **DOCKERHUB_TOKEN**
1. **Primeiro, gere um token no Docker Hub:**
   - Acesse [Docker Hub](https://hub.docker.com)
   - Vá para: Account Settings → Security → New Access Token
   - Nome do token: `gov-hub-ci-cd`
   - Permissões: `Read, Write, Delete`
   - Copie o token gerado (você não conseguirá vê-lo novamente)

2. **No GitHub:**
   - Clique em **"New repository secret"**
   - **Name:** `DOCKERHUB_TOKEN`
   - **Secret:** Cole o token copiado do Docker Hub
   - Clique em **"Add secret"**

### **☁️ AWS - Configuração de Segredos**

#### **AWS_REGION**
1. Clique em **"New repository secret"**
2. **Name:** `AWS_REGION`
3. **Secret:** A região AWS onde você quer fazer deploy (ex: `sa-east-1` para São Paulo)
4. Clique em **"Add secret"**

#### **AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY**

⚠️ **IMPORTANTE:** Use um usuário IAM específico para CI/CD, não suas credenciais pessoais!

1. **Crie um usuário IAM no AWS:**
   - Acesse o AWS Console → IAM → Users → Create user
   - Nome: `gov-hub-ci-cd`
   - Anexe políticas necessárias (ex: `AmazonEC2FullAccess`, `AmazonS3FullAccess`)
   - Gere chaves de acesso: Access key → CLI, SDK, & API access

2. **Configure AWS_ACCESS_KEY_ID:**
   - **Name:** `AWS_ACCESS_KEY_ID`
   - **Secret:** A Access Key ID gerada
   - Clique em **"Add secret"**

3. **Configure AWS_SECRET_ACCESS_KEY:**
   - **Name:** `AWS_SECRET_ACCESS_KEY`
   - **Secret:** A Secret Access Key gerada
   - Clique em **"Add secret"**

---

## ✅ Validação das Configurações

Após configurar todos os segredos, você deve ver:

### **Lista de Segredos Configurados:**
```
DOCKER_USERNAME          ••••••••
DOCKERHUB_TOKEN          ••••••••
AWS_REGION               ••••••••
AWS_ACCESS_KEY_ID        ••••••••
AWS_SECRET_ACCESS_KEY    ••••••••
```

### **Teste dos Pipelines:**
1. Faça um commit pequeno no branch `main`
2. Verifique se os workflows executam sem erros relacionados a segredos
3. Os logs devem mostrar conexões bem-sucedidas aos serviços

---

## 🔧 Troubleshooting

### **Problema: Docker Hub authentication failed**
**Solução:**
- Verifique se `DOCKER_USERNAME` está correto (case-sensitive)
- Regenere o `DOCKERHUB_TOKEN` no Docker Hub
- Certifique-se de que o token tem permissões de escrita

### **Problema: AWS credentials invalid**
**Solução:**
- Verifique se as chaves AWS estão corretas
- Confirme que o usuário IAM tem as permissões necessárias
- Teste as credenciais com AWS CLI localmente

### **Problema: Região AWS não encontrada**
**Solução:**
- Use códigos de região válidos: `us-east-1`, `us-west-2`, `sa-east-1`, etc.
- Verifique se a região suporta os serviços necessários

### **Problema: Segredos não aparecem nos workflows**
**Solução:**
- Aguarde alguns minutos (propagação pode ser lenta)
- Verifique se os nomes dos segredos estão exatamente iguais nos workflows
- Confirme permissões de administrador no repositório

---

## 🛡️ Boas Práticas de Segurança

### **✅ Faça:**
- Use tokens específicos para CI/CD, não credenciais pessoais
- Configure permissões mínimas necessárias
- Monitore o uso dos tokens regularmente
- Renove tokens periodicamente

### **❌ Não Faça:**
- Nunca commite segredos no código
- Não use credenciais de produção para testes
- Não compartilhe tokens em canais inseguros
- Não dê permissões excessivas a usuários IAM

---

## 📞 Suporte

Se você encontrar problemas durante a configuração:

1. **Verifique os logs** dos workflows para mensagens de erro específicas
2. **Consulte a documentação** do serviço específico (Docker Hub, AWS)
3. **Teste localmente** as credenciais antes de configurar no GitHub

---

## 📝 Checklist Final

Antes de considerar a configuração completa, confirme:

- [ ] Todos os 5 segredos estão configurados
- [ ] Os nomes dos segredos estão corretos (case-sensitive)
- [ ] Os tokens/chaves têm permissões adequadas
- [ ] Um workflow de teste foi executado com sucesso
- [ ] Não há erros de autenticação nos logs

---

*Guia atualizado em 26 de junho de 2025*  
*Projeto Gov-Hub - Configuração de CI/CD*
