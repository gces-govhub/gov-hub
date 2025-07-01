#!/usr/bin/env python3
"""
Teste da API do Portal da Transparência
Teste direto para verificar se a chave está funcionando.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_api():
    """Testa diferentes endpoints da API."""
    api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
    print(f"🔑 Chave de API: {api_key[:10]}...")
    
    headers = {
        'chave-api-dados': api_key,
        'Accept': 'application/json'
    }
    
    # Testar endpoint mais simples primeiro
    endpoints = [
        ("Órgãos SIAFI", "https://api.portaldatransparencia.gov.br/api-de-dados/orgaos-siafi", {}),
        ("Despesas Execução", "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/execucao", {
            'mesAnoInicio': '01/2024',
            'mesAnoFim': '01/2024',
            'codigoOrgao': '26000',  # Ministério da Educação
            'pagina': 1,
            'tamanhoPagina': 10
        }),
        ("Servidores", "https://api.portaldatransparencia.gov.br/api-de-dados/servidores", {
            'pagina': 1,
            'tamanhoPagina': 10
        })
    ]
    
    for nome, url, params in endpoints:
        print(f"\n🧪 Testando: {nome}")
        print(f"🔗 URL: {url}")
        print(f"📋 Params: {params}")
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Sucesso! {len(data)} registros recebidos")
                if data:
                    print(f"📄 Primeiro item: {list(data[0].keys()) if isinstance(data, list) and data else 'Estrutura diferente'}")
            else:
                print(f"❌ Erro: {response.status_code}")
                print(f"📝 Response: {response.text[:300]}")
                
        except Exception as e:
            print(f"❌ Exceção: {e}")

if __name__ == "__main__":
    test_api()
