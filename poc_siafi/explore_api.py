#!/usr/bin/env python3
"""
Explorador da API - Ver dados disponíveis
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def explore_orgaos():
    """Explora os órgãos disponíveis."""
    api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
    
    headers = {
        'chave-api-dados': api_key,
        'Accept': 'application/json'
    }
    
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/orgaos-siafi"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            orgaos = response.json()
            print(f"📋 {len(orgaos)} órgãos encontrados:")
            print("=" * 60)
            
            for orgao in orgaos[:10]:  # Primeiros 10
                print(f"🏛️ {orgao['codigo']} - {orgao['descricao']}")
            
            # Salvar lista completa
            with open('data/poc_siafi/relatorios/orgaos_siafi.json', 'w', encoding='utf-8') as f:
                json.dump(orgaos, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Lista completa salva em: orgaos_siafi.json")
            return orgaos
        else:
            print(f"❌ Erro: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def test_other_endpoints():
    """Testa outros endpoints que podem funcionar."""
    api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
    
    headers = {
        'chave-api-dados': api_key,
        'Accept': 'application/json'
    }
    
    # Endpoints que podem funcionar sem filtros complexos
    endpoints = [
        ("Cartões de Pagamento", "https://api.portaldatransparencia.gov.br/api-de-dados/cartoes", {
            'mesAnoInicio': '01/2024',
            'mesAnoFim': '01/2024',
            'pagina': 1,
            'tamanhoPagina': 5
        }),
        ("Transferências", "https://api.portaldatransparencia.gov.br/api-de-dados/transferencias", {
            'mesAnoInicio': '01/2024',
            'mesAnoFim': '01/2024',
            'pagina': 1,
            'tamanhoPagina': 5
        }),
        ("Convênios", "https://api.portaldatransparencia.gov.br/api-de-dados/convenios", {
            'anoConvenio': 2024,
            'pagina': 1,
            'tamanhoPagina': 5
        })
    ]
    
    print("\n🧪 TESTANDO OUTROS ENDPOINTS:")
    print("=" * 60)
    
    for nome, url, params in endpoints:
        print(f"\n📡 {nome}")
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {len(data)} registros recebidos")
                
                # Salvar exemplo
                if data:
                    filename = f"data/poc_siafi/relatorios/exemplo_{nome.lower().replace(' ', '_')}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data[:3], f, indent=2, ensure_ascii=False)
                    print(f"   💾 Exemplo salvo: {filename}")
                    
            else:
                print(f"   ❌ Erro: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")

if __name__ == "__main__":
    print("🏛️ EXPLORADOR DA API DO PORTAL DA TRANSPARÊNCIA")
    print("=" * 60)
    
    # Explorar órgãos
    orgaos = explore_orgaos()
    
    # Testar outros endpoints
    test_other_endpoints()
