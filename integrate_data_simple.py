#!/usr/bin/env python3
"""
Data Integrator Simplificado - Versão que funciona apenas com bibliotecas nativas do Python
Criado para resolver incompatibilidades com Python 3.13
"""

import csv
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleDataIntegrator:
    def __init__(self):
        self.raw_dir = Path('data/raw')
        self.processed_dir = Path('data/processed')
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_csv_data(self, filename):
        """Carrega dados de um arquivo CSV usando apenas csv nativo"""
        filepath = self.raw_dir / filename
        
        if not filepath.exists():
            logger.warning(f"Arquivo {filename} não encontrado")
            return []
            
        data = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            logger.info(f"Carregados {len(data)} registros de {filename}")
        except Exception as e:
            logger.error(f"Erro ao carregar {filename}: {e}")
            
        return data

    def find_latest_files(self):
        """Encontra os arquivos mais recentes de cada fonte"""
        files = {
            'siafi': None,
            'compras': None,
            'transferegov': None
        }
        
        # Procurar arquivos mais recentes
        for file_path in self.raw_dir.glob('*.csv'):
            filename = file_path.name.lower()
            if 'siafi' in filename:
                files['siafi'] = file_path.name
            elif 'contrato' in filename or 'compras' in filename:
                files['compras'] = file_path.name
            elif 'convenio' in filename or 'transfere' in filename:
                files['transferegov'] = file_path.name
                
        return files

    def integrate_data(self):
        """Integra os dados usando lógica simples de matching"""
        files = self.find_latest_files()
        
        # Carregar dados
        siafi_data = self.load_csv_data(files['siafi']) if files['siafi'] else []
        compras_data = self.load_csv_data(files['compras']) if files['compras'] else []
        transfere_data = self.load_csv_data(files['transferegov']) if files['transferegov'] else []
        
        # Criar índices para join eficiente
        compras_index = {row.get('uasg', ''): row for row in compras_data}
        transfere_index = {row.get('codigo_siafi', ''): row for row in transfere_data}
        
        # Integrar dados
        integrated_data = []
        matches = {'siafi_compras': 0, 'siafi_transfere': 0, 'total_integrated': 0}
        
        for siafi_row in siafi_data:
            codigo_ug = siafi_row.get('codigo_ug', '')
            
            # Criar linha integrada começando com dados do SIAFI
            integrated_row = dict(siafi_row)
            
            # Tentar fazer join com compras
            if codigo_ug in compras_index:
                compras_row = compras_index[codigo_ug]
                for key, value in compras_row.items():
                    integrated_row[f'compras_{key}'] = value
                matches['siafi_compras'] += 1
                
            # Tentar fazer join com transferegov
            if codigo_ug in transfere_index:
                transfere_row = transfere_index[codigo_ug]
                for key, value in transfere_row.items():
                    integrated_row[f'transfere_{key}'] = value
                matches['siafi_transfere'] += 1
                
            integrated_data.append(integrated_row)
            matches['total_integrated'] += 1
            
        return integrated_data, matches, {
            'siafi': len(siafi_data),
            'compras': len(compras_data),
            'transferegov': len(transfere_data)
        }

    def save_integrated_data(self, integrated_data):
        """Salva os dados integrados em CSV"""
        if not integrated_data:
            logger.warning("Nenhum dado para salvar")
            return False
            
        output_file = self.processed_dir / 'integrated_poc_data.csv'
        
        try:
            # Obter todas as colunas únicas
            all_columns = set()
            for row in integrated_data:
                all_columns.update(row.keys())
            all_columns = sorted(list(all_columns))
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=all_columns)
                writer.writeheader()
                writer.writerows(integrated_data)
                
            logger.info(f"Dados integrados salvos em {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar dados integrados: {e}")
            return False

    def generate_summary(self, matches, counts):
        """Gera relatório de resumo da integração"""
        summary_lines = [
            "=== Resumo da Integracao de Dados ===",
            "",
            f"Data/Hora da Execucao: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "Fontes de Dados:",
            f"- SIAFI: {counts['siafi']} registros",
            f"- Compras.gov.br: {counts['compras']} registros", 
            f"- TransfereGov: {counts['transferegov']} registros",
            "",
            "Resultados da Integracao:",
            f"- Total de registros integrados: {matches['total_integrated']}",
            f"- Correspondencias SIAFI-Compras: {matches['siafi_compras']}",
            f"- Correspondencias SIAFI-TransfereGov: {matches['siafi_transfere']}",
            "",
            "Taxa de Correspondencia:",
            f"- SIAFI-Compras: {(matches['siafi_compras']/max(counts['siafi'], 1)*100):.1f}%",
            f"- SIAFI-TransfereGov: {(matches['siafi_transfere']/max(counts['siafi'], 1)*100):.1f}%",
            "",
            "Status: INTEGRACAO CONCLUIDA COM SUCESSO!",
            "",
            "Arquivos Gerados:",
            "- data/processed/integrated_poc_data.csv (dados integrados)",
            "- data/processed/poc_summary.txt (este relatorio)"
        ]
        
        summary_file = self.processed_dir / 'poc_summary.txt'
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(summary_lines))
            logger.info(f"Relatorio salvo em {summary_file}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar relatorio: {e}")
            return False

def main():
    integrator = SimpleDataIntegrator()
    
    try:
        logger.info("=== Iniciando integracao de dados ===")
        
        # Integrar dados
        integrated_data, matches, counts = integrator.integrate_data()
        
        if not integrated_data:
            logger.error("Nenhum dado foi integrado")
            return False
            
        # Salvar dados integrados
        if integrator.save_integrated_data(integrated_data):
            logger.info("Dados integrados salvos com sucesso")
        else:
            logger.error("Falha ao salvar dados integrados")
            return False
            
        # Gerar resumo
        if integrator.generate_summary(matches, counts):
            logger.info("Relatorio de resumo gerado com sucesso")
        else:
            logger.warning("Falha ao gerar relatorio de resumo")
            
        logger.info("=== Integracao concluida ===")
        return True
        
    except Exception as e:
        logger.error(f"Erro durante a integracao: {e}")
        return False

if __name__ == '__main__':
    main()
