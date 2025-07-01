#!/usr/bin/env python3
"""
Aquisição de Dados Reais do SIAFI - Portal da Transparência
Sistema para coletar dados reais do SIAFI via API oficial do governo.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import logging
import time
import json
import os
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SiafiRealDataCollector:
    """Coletor de dados reais do SIAFI via Portal da Transparência."""
    
    def __init__(self):
        """Inicializa o coletor de dados reais."""
        self.base_url = "https://api.portaldatransparencia.gov.br/api-de-dados"
        self.base_dir = Path("data/poc_siafi")
        self.raw_dir = self.base_dir / "dados_brutos"
        self.processed_dir = self.base_dir / "dados_processados"
        self.reports_dir = self.base_dir / "relatorios"
        
        # Criar diretórios
        for dir_path in [self.raw_dir, self.processed_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Headers para requisições
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Gov-Hub-PoC/1.0 (Pesquisa-Academica)'
        }
        
        # Verificar se há chave de API
        self.api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
        if self.api_key:
            self.headers['chave-api-dados'] = self.api_key
            logger.info("🔑 Chave de API encontrada")
        else:
            logger.warning("⚠️ Nenhuma chave de API encontrada. Algumas funcionalidades podem ter limitações.")
    
    def get_despesas_execucao(self, ano: int = 2024, mes: int = None, pagina: int = 1) -> Optional[Dict]:
        """
        Busca dados reais de execução de despesas do SIAFI.
        
        Args:
            ano: Ano da consulta
            mes: Mês específico (opcional)
            pagina: Página da consulta
        """
        endpoint = f"{self.base_url}/despesas/execucao"
        
        # Parâmetros da consulta - formato correto da API
        params = {
            'mesAnoInicio': f"{mes:02d}/{ano}" if mes else f"01/{ano}",
            'mesAnoFim': f"{mes:02d}/{ano}" if mes else f"12/{ano}",
            'pagina': pagina,
            'tamanhoPagina': 500  # Máximo permitido
        }
        
        try:
            logger.info(f"📡 Consultando API SIAFI - Ano: {ano}, Mês: {mes or 'Todos'}, Página: {pagina}")
            logger.info(f"🔗 Endpoint: {endpoint}")
            logger.info(f"📋 Parâmetros: {params}")
            
            response = requests.get(
                endpoint, 
                params=params, 
                headers=self.headers, 
                timeout=30
            )
            
            logger.info(f"📡 Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Resposta recebida: {len(data)} registros")
                return data
            elif response.status_code == 429:
                logger.warning("⏳ Rate limit atingido. Aguardando...")
                time.sleep(60)
                return self.get_despesas_execucao(ano, mes, pagina)
            else:
                logger.error(f"❌ Erro na API: {response.status_code}")
                logger.error(f"Response: {response.text[:1000]}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro na requisição: {e}")
            return None
    
    def get_orgaos_siafi(self) -> Optional[List[Dict]]:
        """Busca lista de órgãos do SIAFI."""
        endpoint = f"{self.base_url}/orgaos-siafi"
        
        try:
            logger.info("📋 Buscando lista de órgãos SIAFI...")
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ {len(data)} órgãos encontrados")
                return data
            else:
                logger.error(f"❌ Erro ao buscar órgãos: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na busca de órgãos: {e}")
            return None
    
    def collect_real_data(self, ano: int = 2024, mes: int = None, max_pages: int = 5) -> Optional[Path]:
        """
        Coleta dados reais do SIAFI.
        
        Args:
            ano: Ano da consulta
            mes: Mês específico (opcional)
            max_pages: Máximo de páginas a coletar
        """
        logger.info(f"🏛️ Iniciando coleta de dados REAIS do SIAFI")
        logger.info(f"📅 Período: {mes or 'Ano completo'}/{ano}")
        
        all_data = []
        pagina = 1
        
        while pagina <= max_pages:
            # Buscar dados da página
            data = self.get_despesas_execucao(ano, mes, pagina)
            
            if not data:
                logger.warning(f"⚠️ Sem dados na página {pagina}")
                break
            
            # Verificar se há dados na resposta
            if isinstance(data, list) and len(data) == 0:
                logger.info(f"📄 Página {pagina} vazia - fim dos dados")
                break
            
            # Adicionar dados
            if isinstance(data, list):
                all_data.extend(data)
                logger.info(f"📋 Página {pagina}: {len(data)} registros coletados")
            else:
                logger.warning(f"⚠️ Formato inesperado de dados na página {pagina}")
                break
            
            # Se recebeu menos que o máximo, provavelmente é a última página
            if len(data) < 500:
                logger.info(f"📄 Página {pagina} com {len(data)} registros - fim dos dados")
                break
            
            pagina += 1
            time.sleep(2)  # Rate limiting respeitoso
        
        if all_data:
            # Salvar dados coletados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Arquivo JSON bruto
            json_file = self.raw_dir / f"siafi_real_{ano}_{mes or 'completo'}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            
            # Arquivo CSV processado
            csv_file = self.raw_dir / f"siafi_real_{ano}_{mes or 'completo'}_{timestamp}.csv"
            df = pd.DataFrame(all_data)
            df.to_csv(csv_file, index=False, encoding='utf-8')
            
            logger.info(f"💾 Dados salvos:")
            logger.info(f"  📄 JSON: {json_file.name}")
            logger.info(f"  📊 CSV: {csv_file.name}")
            logger.info(f"✅ Total coletado: {len(all_data):,} registros REAIS do SIAFI")
            
            # Gerar relatório da coleta
            self.generate_collection_report(csv_file, all_data, ano, mes)
            
            return csv_file
        else:
            logger.error("❌ Nenhum dado real foi coletado")
            return None
    
    def generate_collection_report(self, csv_file: Path, data: List[Dict], ano: int, mes: Optional[int]):
        """Gera relatório detalhado da coleta de dados reais."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"relatorio_coleta_real_{timestamp}.txt"
        
        df = pd.DataFrame(data)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE COLETA - DADOS REAIS DO SIAFI\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"🕒 Data da Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"🌐 Fonte: Portal da Transparência - API Oficial\n")
            f.write(f"📅 Período: {mes or 'Ano completo'}/{ano}\n")
            f.write(f"📁 Arquivo: {csv_file.name}\n")
            f.write(f"🔑 API Key: {'Presente' if self.api_key else 'Não configurada'}\n\n")
            
            f.write("📊 ESTATÍSTICAS DA COLETA:\n")
            f.write("-" * 50 + "\n")
            f.write(f"📋 Total de registros: {len(data):,}\n")
            f.write(f"💾 Tamanho do arquivo: {csv_file.stat().st_size / 1024:.2f} KB\n")
            f.write(f"🗂️ Colunas disponíveis: {len(df.columns) if not df.empty else 0}\n\n")
            
            if not df.empty:
                f.write("🏗️ ESTRUTURA DOS DADOS:\n")
                f.write("-" * 50 + "\n")
                for i, col in enumerate(df.columns, 1):
                    f.write(f"{i:2d}. {col}\n")
                
                # Análise de valores se existir coluna de valor
                valor_cols = [col for col in df.columns if 'valor' in col.lower() or 'vlr' in col.lower()]
                if valor_cols:
                    col_valor = valor_cols[0]
                    f.write(f"\n💰 ANÁLISE FINANCEIRA (coluna: {col_valor}):\n")
                    f.write("-" * 50 + "\n")
                    try:
                        valores = pd.to_numeric(df[col_valor], errors='coerce')
                        f.write(f"💵 Valor total: R$ {valores.sum():,.2f}\n")
                        f.write(f"📊 Valor médio: R$ {valores.mean():,.2f}\n")
                        f.write(f"📈 Valor máximo: R$ {valores.max():,.2f}\n")
                        f.write(f"📉 Valor mínimo: R$ {valores.min():,.2f}\n")
                    except:
                        f.write("⚠️ Não foi possível analisar valores financeiros\n")
                
                f.write(f"\n📋 AMOSTRA DOS DADOS (primeiros 3 registros):\n")
                f.write("-" * 50 + "\n")
                for i, (_, row) in enumerate(df.head(3).iterrows()):
                    f.write(f"\n🔹 Registro {i+1}:\n")
                    for col, val in row.items():
                        f.write(f"   {col}: {val}\n")
            
            f.write(f"\n✅ COLETA DE DADOS REAIS CONCLUÍDA!\n")
            f.write(f"🎯 Dados autênticos do SIAFI prontos para análise.\n")
            f.write(f"📡 Fonte oficial: Portal da Transparência do Governo Federal\n")
        
        logger.info(f"📋 Relatório detalhado salvo: {report_file.name}")

def main():
    """Função principal para coleta de dados reais."""
    print("🏛️ Gov-Hub - Coletor de Dados Reais do SIAFI")
    print("=" * 60)
    
    # Instruções para API Key
    if not os.getenv('PORTAL_TRANSPARENCIA_API_KEY'):
        print("\n⚠️  IMPORTANTE: Para melhor performance, configure sua chave de API:")
        print("1. Acesse: https://api.portaltransparencia.gov.br/")
        print("2. Solicite sua chave gratuita")
        print("3. Configure: set PORTAL_TRANSPARENCIA_API_KEY=sua_chave")
        print("4. Ou crie arquivo .env com: PORTAL_TRANSPARENCIA_API_KEY=sua_chave")
        print("\n📝 Continuando sem chave (com limitações)...\n")
    
    collector = SiafiRealDataCollector()
    
    try:
        # Coletar dados de 2024 (ano com dados confirmados)
        ano_dados = 2024
        mes_dados = 12  # Dezembro de 2024
        
        logger.info(f"🚀 Iniciando coleta de dados reais do SIAFI...")
        logger.info(f"📅 Buscando dados de {mes_dados:02d}/{ano_dados}")
        
        # Coletar dados
        arquivo = collector.collect_real_data(
            ano=ano_dados,
            mes=mes_dados,
            max_pages=5  # Aumentar para mais dados
        )
        
        if arquivo:
            print(f"\n✅ COLETA CONCLUÍDA COM SUCESSO!")
            print(f"📁 Arquivo: {arquivo.name}")
            print(f"📊 Dados reais do SIAFI coletados e organizados")
            print(f"📋 Verifique os relatórios em: data/poc_siafi/relatorios/")
        else:
            print("\n❌ FALHA NA COLETA")
            print("💡 Verifique:")
            print("   - Conexão com internet")
            print("   - Disponibilidade da API")
            print("   - Configuração da chave de API")
            
    except Exception as e:
        logger.error(f"❌ Erro na execução: {e}")
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()
