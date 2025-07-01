#!/usr/bin/env python3
"""
Aquisição de Dados Reais do SIAFI - Gov-Hub PoC
Script para baixar dados reais do Portal da Transparência do SIAFI.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import logging
import time
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RealSiafiAcquirer:
    """Classe para aquisição de dados reais do SIAFI via Portal da Transparência."""
    
    def __init__(self):
        self.base_url = "https://api.portaldatransparencia.gov.br/api-de-dados"
        self.base_dir = Path("data/poc_siafi")
        self.raw_dir = self.base_dir / "dados_brutos"
        self.processed_dir = self.base_dir / "dados_processados"
        self.reports_dir = self.base_dir / "relatorios"
        
        # Criar diretórios
        for dir_path in [self.raw_dir, self.processed_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_despesas_execucao(self, ano=2024, mes=12, pagina=1, limite=500):
        """
        Busca dados de despesas de execução do SIAFI.
        
        Args:
            ano: Ano dos dados (padrão: 2024)
            mes: Mês dos dados (padrão: 12)
            pagina: Página da consulta (padrão: 1)
            limite: Limite de registros por página (máximo: 500)
        """
        url = f"{self.base_url}/despesas/execucao"
        
        params = {
            'mesAnoInicio': f"{mes:02d}/{ano}",
            'mesAnoFim': f"{mes:02d}/{ano}",
            'pagina': pagina,
            'tamanhoPagina': limite
        }
        
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Gov-Hub-PoC/1.0'
        }
        
        try:
            logger.info(f"📊 Buscando dados SIAFI - Ano: {ano}, Mês: {mes}, Página: {pagina}")
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Erro na API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na requisição: {e}")
            return None
    
    def collect_sample_data(self, ano=2024, mes=12, max_registros=1000):
        """
        Coleta uma amostra de dados reais do SIAFI.
        
        Args:
            ano: Ano dos dados
            mes: Mês dos dados
            max_registros: Máximo de registros a coletar
        """
        logger.info(f"🏛️ Iniciando coleta de dados reais do SIAFI...")
        logger.info(f"📅 Período: {mes:02d}/{ano}")
        
        all_data = []
        pagina = 1
        registros_coletados = 0
        
        while registros_coletados < max_registros:
            # Calcular limite para esta página
            limite = min(500, max_registros - registros_coletados)
            
            # Buscar dados
            data = self.get_despesas_execucao(ano, mes, pagina, limite)
            
            if not data or not data.get('data'):
                logger.warning(f"⚠️ Sem dados na página {pagina}")
                break
            
            page_data = data.get('data', [])
            all_data.extend(page_data)
            registros_coletados += len(page_data)
            
            logger.info(f"📋 Página {pagina}: {len(page_data)} registros coletados (Total: {registros_coletados})")
            
            # Verificar se há mais páginas
            if len(page_data) < limite:
                break
            
            pagina += 1
            time.sleep(1)  # Rate limiting
        
        if all_data:
            # Salvar dados brutos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_file = self.raw_dir / f"siafi_despesas_reais_{ano}_{mes:02d}_{timestamp}.json"
            
            with open(raw_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Dados brutos salvos: {raw_file.name}")
            
            # Converter para CSV
            csv_file = self.raw_dir / f"siafi_despesas_reais_{ano}_{mes:02d}_{timestamp}.csv"
            df = pd.DataFrame(all_data)
            df.to_csv(csv_file, index=False, encoding='utf-8')
            
            logger.info(f"📊 CSV criado: {csv_file.name}")
            logger.info(f"✅ Total coletado: {len(all_data)} registros reais do SIAFI")
            
            # Gerar relatório
            self.generate_collection_report(csv_file, all_data)
            
            return csv_file
        else:
            logger.error("❌ Nenhum dado foi coletado")
            return None
    
    def generate_collection_report(self, csv_file, data):
        """Gera relatório da coleta de dados."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"relatorio_coleta_siafi_{timestamp}.txt"
        
        # Análise básica dos dados
        df = pd.DataFrame(data)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE COLETA - DADOS REAIS DO SIAFI\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Data da Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Fonte: Portal da Transparência - API SIAFI\n")
            f.write(f"Arquivo: {csv_file.name}\n\n")
            
            f.write("ESTATÍSTICAS DA COLETA:\n")
            f.write("-" * 40 + "\n")
            f.write(f"📊 Total de registros: {len(data):,}\n")
            f.write(f"📁 Tamanho do arquivo: {csv_file.stat().st_size / 1024:.2f} KB\n")
            f.write(f"🗃️ Colunas disponíveis: {len(df.columns)}\n\n")
            
            f.write("ESTRUTURA DOS DADOS:\n")
            f.write("-" * 40 + "\n")
            for i, col in enumerate(df.columns, 1):
                f.write(f"{i:2d}. {col}\n")
            
            if not df.empty:
                f.write("\nAMOSTRA DOS DADOS (primeiros 3 registros):\n")
                f.write("-" * 40 + "\n")
                for i, (_, row) in enumerate(df.head(3).iterrows()):
                    f.write(f"\nRegistro {i+1}:\n")
                    for col, val in row.items():
                        f.write(f"  {col}: {val}\n")
            
            f.write(f"\n✅ COLETA CONCLUÍDA COM SUCESSO!\n")
            f.write(f"🎯 Dados reais do SIAFI prontos para análise.\n")
        
        logger.info(f"📋 Relatório de coleta salvo: {report_file.name}")

def main():
    """Função principal para coleta de dados."""
    acquirer = RealSiafiAcquirer()
    
    try:
        # Coletar dados do mês anterior
        hoje = datetime.now()
        mes_anterior = hoje.replace(day=1) - timedelta(days=1)
        
        logger.info(f"🚀 Iniciando coleta de dados reais do SIAFI...")
        
        # Tentar coletar dados recentes
        arquivo = acquirer.collect_sample_data(
            ano=mes_anterior.year, 
            mes=mes_anterior.month, 
            max_registros=1000
        )
        
        if arquivo:
            logger.info(f"✅ Coleta concluída! Arquivo: {arquivo.name}")
        else:
            logger.error("❌ Falha na coleta de dados")
            
    except Exception as e:
        logger.error(f"❌ Erro na execução: {e}")

if __name__ == "__main__":
    main()
