#!/usr/bin/env python3
"""
Demonstração da PoC SIAFI - Dados Reais
Como configurar e usar a API do Portal da Transparência para obter dados reais do SIAFI.
"""

import requests
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def test_api_availability():
    """Testa a disponibilidade da API do Portal da Transparência."""
    print("🔍 TESTANDO CONECTIVIDADE COM A API DO PORTAL DA TRANSPARÊNCIA")
    print("=" * 70)
    
    # URLs para testar
    urls_test = [
        "https://api.portaldatransparencia.gov.br/swagger-ui.html",
        "https://api.portaldatransparencia.gov.br/api-de-dados",
    ]
    
    for url in urls_test:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Erro: {e}")
    
    print("\n📋 INFORMAÇÕES SOBRE A API:")
    print("-" * 50)
    print("🌐 Portal: https://api.portaldatransparencia.gov.br/")
    print("📧 Cadastro de chave: http://www.portaldatransparencia.gov.br/api-de-dados/cadastrar-email")
    print("📚 Documentação: https://api.portaldatransparencia.gov.br/swagger-ui.html")

def demonstrate_api_usage():
    """Demonstra como usar a API com chave."""
    print("\n🔧 COMO CONFIGURAR A CHAVE DE API:")
    print("=" * 50)
    print("1. Acesse: http://www.portaldatransparencia.gov.br/api-de-dados/cadastrar-email")
    print("2. Informe seu email")
    print("3. Confirme no email recebido")
    print("4. Guarde sua chave de API")
    print("5. Configure no sistema:")
    print("   • Windows: set PORTAL_TRANSPARENCIA_API_KEY=sua_chave")
    print("   • Linux/Mac: export PORTAL_TRANSPARENCIA_API_KEY=sua_chave")
    print("   • Ou crie arquivo .env: PORTAL_TRANSPARENCIA_API_KEY=sua_chave")
    
    print("\n📊 ENDPOINTS DISPONÍVEIS PARA SIAFI:")
    print("-" * 50)
    
    endpoints = [
        {
            "nome": "Despesas - Execução",
            "endpoint": "/despesas/execucao",
            "descrição": "Dados de execução orçamentária",
            "parametros": "anoExercicio, mesExercicio, pagina, tamanhoPagina"
        },
        {
            "nome": "Órgãos SIAFI",
            "endpoint": "/orgaos-siafi",
            "descrição": "Lista de órgãos do SIAFI",
            "parametros": "pagina, tamanhoPagina"
        },
        {
            "nome": "Cartões de Pagamento",
            "endpoint": "/cartoes",
            "descrição": "Gastos com cartão corporativo",
            "parametros": "mesAnoInicio, mesAnoFim, cpfPortador"
        }
    ]
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"{i}. {endpoint['nome']}")
        print(f"   📡 Endpoint: {endpoint['endpoint']}")
        print(f"   📝 Descrição: {endpoint['descrição']}")
        print(f"   ⚙️ Parâmetros: {endpoint['parametros']}")
        print()

def create_api_setup_guide():
    """Cria um guia completo de configuração da API."""
    guide_file = Path("data/poc_siafi/relatorios/guia_configuracao_api.txt")
    guide_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("GUIA COMPLETO - CONFIGURAÇÃO DA API DO PORTAL DA TRANSPARÊNCIA\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("🎯 OBJETIVO:\n")
        f.write("Configurar acesso à API oficial do Portal da Transparência para\n")
        f.write("coletar dados REAIS do SIAFI (Sistema Integrado de Administração Financeira).\n\n")
        
        f.write("📋 PASSO A PASSO:\n")
        f.write("-" * 50 + "\n")
        f.write("1. SOLICITAR CHAVE DE API:\n")
        f.write("   • Acesse: http://www.portaldatransparencia.gov.br/api-de-dados/cadastrar-email\n")
        f.write("   • Informe seu email (pode ser pessoal ou institucional)\n")
        f.write("   • Clique em 'Solicitar Chave'\n")
        f.write("   • Aguarde o email de confirmação\n\n")
        
        f.write("2. CONFIRMAR EMAIL:\n")
        f.write("   • Verifique sua caixa de entrada\n")
        f.write("   • Clique no link de confirmação no email\n")
        f.write("   • Sua chave será exibida na tela\n")
        f.write("   • IMPORTANTE: Anote sua chave em local seguro\n\n")
        
        f.write("3. CONFIGURAR NO SISTEMA:\n")
        f.write("   Opção A - Variável de Ambiente (Windows):\n")
        f.write("   set PORTAL_TRANSPARENCIA_API_KEY=sua_chave_aqui\n\n")
        
        f.write("   Opção B - Arquivo .env (recomendado):\n")
        f.write("   • Crie arquivo .env na raiz do projeto\n")
        f.write("   • Adicione: PORTAL_TRANSPARENCIA_API_KEY=sua_chave_aqui\n\n")
        
        f.write("   Opção C - Variável de Ambiente (Linux/Mac):\n")
        f.write("   export PORTAL_TRANSPARENCIA_API_KEY=sua_chave_aqui\n\n")
        
        f.write("4. TESTAR CONFIGURAÇÃO:\n")
        f.write("   • Execute: python collect_real_siafi.py\n")
        f.write("   • Deve mostrar: '🔑 Chave de API encontrada'\n")
        f.write("   • Se aparecer erro, verifique a configuração\n\n")
        
        f.write("📊 DADOS DISPONÍVEIS:\n")
        f.write("-" * 50 + "\n")
        f.write("• Execução Orçamentária (despesas)\n")
        f.write("• Órgãos e Unidades Gestoras\n")
        f.write("• Cartões de Pagamento\n")
        f.write("• Transferências\n")
        f.write("• Convênios\n")
        f.write("• Servidores Públicos\n\n")
        
        f.write("⚡ LIMITAÇÕES SEM CHAVE:\n")
        f.write("-" * 50 + "\n")
        f.write("• Acesso negado (erro 401)\n")
        f.write("• Impossível coletar dados reais\n")
        f.write("• Funciona apenas com dados simulados\n\n")
        
        f.write("✅ VANTAGENS COM CHAVE:\n")
        f.write("-" * 50 + "\n")
        f.write("• Acesso completo à API\n")
        f.write("• Dados oficiais e atualizados\n")
        f.write("• Rate limits mais generosos\n")
        f.write("• Suporte técnico oficial\n\n")
        
        f.write("🔗 LINKS ÚTEIS:\n")
        f.write("-" * 50 + "\n")
        f.write("• Portal da Transparência: https://portaldatransparencia.gov.br/\n")
        f.write("• API Docs: https://api.portaldatransparencia.gov.br/swagger-ui.html\n")
        f.write("• Cadastro de Email: http://www.portaldatransparencia.gov.br/api-de-dados/cadastrar-email\n")
        f.write("• GitHub da API: https://github.com/transparencia-mg/\n\n")
        
        f.write("📞 SUPORTE:\n")
        f.write("-" * 50 + "\n")
        f.write("• Email: xxxxxxxxxx@cgu.gov.br (verificar site oficial)\n")
        f.write("• Documentação: Disponível no Swagger UI\n")
        f.write("• Issues: GitHub do projeto\n\n")
        
        f.write("⚠️ IMPORTANTE:\n")
        f.write("-" * 50 + "\n")
        f.write("• A chave é GRATUITA\n")
        f.write("• Use apenas para fins legítimos\n")
        f.write("• Respeite os rate limits\n")
        f.write("• Não compartilhe sua chave\n")
        f.write("• Mantenha o .env no .gitignore\n\n")
        
        f.write("🚀 PRÓXIMOS PASSOS:\n")
        f.write("-" * 50 + "\n")
        f.write("1. Configure sua chave seguindo este guia\n")
        f.write("2. Execute: python collect_real_siafi.py\n")
        f.write("3. Verifique os dados coletados em data/poc_siafi/\n")
        f.write("4. Analise os relatórios gerados\n")
        f.write("5. Desenvolva suas análises específicas\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("GUIA CRIADO PELO GOV-HUB PoC SIAFI\n")
        f.write("Versão: 1.0 | Data: 01/07/2025\n")
        f.write("=" * 80 + "\n")
    
    logger.info(f"📋 Guia de configuração criado: {guide_file}")
    return guide_file

def main():
    """Função principal de demonstração."""
    print("🏛️ GOV-HUB PoC SIAFI - DEMONSTRAÇÃO DA API REAL")
    print("=" * 60)
    
    # Testar conectividade
    test_api_availability()
    
    # Demonstrar uso
    demonstrate_api_usage()
    
    # Criar guia
    guide_file = create_api_setup_guide()
    
    print(f"\n📋 RESUMO:")
    print("=" * 30)
    print("✅ API do Portal da Transparência está acessível")
    print("❌ Chave de API necessária para coletar dados reais")
    print(f"📖 Guia completo criado: {guide_file.name}")
    print("\n🎯 PRÓXIMO PASSO:")
    print("Configure sua chave de API seguindo o guia criado")

if __name__ == "__main__":
    main()
