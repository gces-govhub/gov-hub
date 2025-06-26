#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from datetime import datetime
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataAcquirer:
    def __init__(self):
        self.output_dir = Path('data/raw')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download_siafi_data(self):
        """
        Downloads SIAFI data from Tesouro Transparente portal.
        Note: Real-time API access requires Serpro contract
        """
        logger.warning("AVISO: O acesso à API SIAFI em tempo real requer um contrato formal com o Serpro. "
                      "Esta PoC utiliza o dump público de dados em CSV.")
        
        # URL do arquivo CSV de exemplo do Portal da Transparência
        # Este é um arquivo real de Execução de Despesas do Portal da Transparência
        url = "https://www.portaltransparencia.gov.br/download-de-dados/despesas/2023"
        
        try:
            logger.info(f"Baixando dados do SIAFI de {url}")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            output_file = self.output_dir / f"siafi_{datetime.now().strftime('%Y-%m-%d')}.csv"
            
            # Download do arquivo em chunks para lidar com arquivos grandes
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            logger.info(f"Dados do SIAFI salvos em {output_file}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar dados do SIAFI: {e}")
            return False

    def download_compras_data(self):
        """Downloads data from Compras.gov.br API"""
        base_url = "https://compras.dados.gov.br/api/v1"
        endpoints = {
            'contratos': '/contratos/doc/',
            'licitacoes': '/licitacoes/doc/'
        }
        
        for resource, endpoint in endpoints.items():
            logger.info(f"Downloading {resource} data...")
            page = 1
            while True:
                response = requests.get(f"{base_url}{endpoint}?page={page}")
                if response.status_code != 200:
                    break
                    
                data = response.json()
                if not data.get('results'):
                    break
                    
                df = pd.DataFrame(data['results'])
                output_file = self.output_dir / f"{resource}_{datetime.now().strftime('%Y-%m-%d')}.csv"
                df.to_csv(output_file, index=False)
                
                page += 1
        return True

    def download_transferegov_data(self):
        """Downloads data from TransfereGov API using PostgREST syntax"""
        base_url = "https://api.transferegov.gestao.gov.br"
        endpoints = {
            'convenios': '/transferenciasespeciais/convenios?select=*',
            'pagamentos': '/fundoafundo/pagamentos?select=*'
        }
        
        for resource, endpoint in endpoints.items():
            logger.info(f"Downloading {resource} data...")
            response = requests.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                df = pd.DataFrame(response.json())
                output_file = self.output_dir / f"{resource}_{datetime.now().strftime('%Y-%m-%d')}.csv"
                df.to_csv(output_file, index=False)
            else:
                logger.error(f"Failed to download {resource} data: {response.status_code}")
        return True

def main():
    parser = argparse.ArgumentParser(description='Download data from government sources')
    parser.add_argument('--source', choices=['siafi', 'compras', 'transferegov', 'all'],
                      help='Specify the data source to download from')
    
    args = parser.parse_args()
    acquirer = DataAcquirer()
    
    if args.source == 'all' or args.source == 'siafi':
        acquirer.download_siafi_data()
    if args.source == 'all' or args.source == 'compras':
        acquirer.download_compras_data()
    if args.source == 'all' or args.source == 'transferegov':
        acquirer.download_transferegov_data()

if __name__ == '__main__':
    main()
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
