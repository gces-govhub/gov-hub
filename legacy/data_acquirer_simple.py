#!/usr/bin/env python3
"""
Data Acquirer Simplificado - Versão que funciona apenas com bibliotecas nativas do Python
Criado para resolver incompatibilidades com Python 3.13
"""

import argparse
import logging
import json
import csv
import ssl
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Configuração de SSL para evitar erros de certificado
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleDataAcquirer:
    def __init__(self):
        self.output_dir = Path('data/raw')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download_siafi_data(self):
        """Cria dados de amostra do SIAFI (sem acesso real à API)"""
        logger.info("Criando dados de amostra do SIAFI...")
        
        sample_data = [
            ["codigo_ug", "orgao", "gestao", "numero_empenho", "valor_empenhado", "credor"],
            ["153978", "26291", "15256", "2023NE000123", "150000.00", "12345678901234"],
            ["153979", "26291", "15256", "2023NE000124", "75000.50", "98765432109876"],
            ["154357", "26291", "15256", "2023NE000125", "200000.00", "45678901234567"],
            ["154358", "26291", "15256", "2023NE000126", "95000.75", "32109876543210"],
            ["154359", "26291", "15256", "2023NE000127", "180000.25", "78901234567890"]
        ]
        
        output_file = self.output_dir / f"siafi_{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
            
        logger.info(f"Dados de amostra do SIAFI salvos em {output_file}")
        return True

    def download_compras_data(self):
        """Cria dados de amostra de Compras.gov.br"""
        logger.info("Criando dados de amostra de Compras.gov.br...")
        
        sample_data = [
            ["uasg", "id_contrato", "valor_total", "cnpj_contratada", "objeto_contrato"],
            ["153978", "2023/001", "150000.00", "12345678901234", "Servicos de TI"],
            ["153979", "2023/002", "75000.50", "98765432109876", "Manutencao Predial"],
            ["154357", "2023/003", "200000.00", "45678901234567", "Consultoria Especializada"],
            ["154358", "2023/004", "95000.75", "32109876543210", "Material de Escritorio"],
            ["154359", "2023/005", "180000.25", "78901234567890", "Equipamentos de Informatica"]
        ]
        
        output_file = self.output_dir / f"contratos_{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
            
        logger.info(f"Dados de amostra de Compras salvos em {output_file}")
        return True

    def download_transferegov_data(self):
        """Cria dados de amostra do TransfereGov"""
        logger.info("Criando dados de amostra do TransfereGov...")
        
        sample_data = [
            ["codigo_siafi", "convenio", "valor_liberado", "data_liberacao", "beneficiario"],
            ["153978", "123456", "150000.00", "2023-01-15", "Municipio A"],
            ["153979", "123457", "75000.50", "2023-02-20", "Municipio B"],
            ["154357", "123458", "200000.00", "2023-03-10", "Municipio C"],
            ["154358", "123459", "95000.75", "2023-04-05", "Municipio D"],
            ["154359", "123460", "180000.25", "2023-05-12", "Municipio E"]
        ]
        
        output_file = self.output_dir / f"convenios_{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
            
        logger.info(f"Dados de amostra do TransfereGov salvos em {output_file}")
        return True

def main():
    parser = argparse.ArgumentParser(description='Download data from government sources (Sample Mode)')
    parser.add_argument('--source', choices=['siafi', 'compras', 'transferegov', 'all'],
                      help='Specify the data source to download from')
    
    args = parser.parse_args()
    acquirer = SimpleDataAcquirer()
    
    try:
        if args.source == 'all' or args.source == 'siafi':
            logger.info("=== Iniciando criacao de dados de amostra do SIAFI ===")
            acquirer.download_siafi_data()
                
        if args.source == 'all' or args.source == 'compras':
            logger.info("=== Iniciando criacao de dados de amostra de Compras.gov.br ===")
            acquirer.download_compras_data()
                
        if args.source == 'all' or args.source == 'transferegov':
            logger.info("=== Iniciando criacao de dados de amostra do TransfereGov ===")
            acquirer.download_transferegov_data()
                
        logger.info("=== Processo de aquisicao de dados finalizado ===")
        return True
        
    except Exception as e:
        logger.error(f"Erro nao tratado durante a aquisicao de dados: {e}")
        return False

if __name__ == '__main__':
    main()
