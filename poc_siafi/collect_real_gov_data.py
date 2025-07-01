#!/usr/bin/env python3
"""
Coletor de Dados Reais - Portal da Transparência
Coleta dados reais de cartões de pagamento e órgãos do governo.
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

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TransparenciaRealCollector:
    """Coletor de dados reais do Portal da Transparência."""
    
    def __init__(self):
        """Inicializa o coletor."""
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
            'chave-api-dados': os.getenv('PORTAL_TRANSPARENCIA_API_KEY'),
            'Accept': 'application/json'
        }
        
        logger.info("🔑 Coletor configurado com chave de API")
    
    def get_orgaos_siafi(self) -> Optional[List[Dict]]:
        """Coleta lista de órgãos SIAFI."""
        endpoint = f"{self.base_url}/orgaos-siafi"
        
        try:
            logger.info("📋 Coletando órgãos SIAFI...")
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ {len(data)} órgãos coletados")
                return data
            else:
                logger.error(f"❌ Erro ao coletar órgãos: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na coleta de órgãos: {e}")
            return None
    
    def get_cartoes_pagamento(self, orgao_codigo: str, mes_ano: str, pagina: int = 1) -> Optional[List[Dict]]:
        """
        Coleta dados de cartões de pagamento de um órgão específico.
        
        Args:
            orgao_codigo: Código do órgão
            mes_ano: Período no formato MM/AAAA
            pagina: Página da consulta
        """
        endpoint = f"{self.base_url}/cartoes"
        
        params = {
            'mesAnoInicio': mes_ano,
            'mesAnoFim': mes_ano,
            'codigoOrgao': orgao_codigo,
            'pagina': pagina,
            'tamanhoPagina': 500
        }
        
        try:
            logger.info(f"💳 Coletando cartões - Órgão: {orgao_codigo}, Período: {mes_ano}, Página: {pagina}")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ {len(data)} registros de cartões coletados")
                return data
            elif response.status_code == 400:
                logger.warning(f"⚠️ Sem dados para órgão {orgao_codigo} no período {mes_ano}")
                return []
            else:
                logger.error(f"❌ Erro na coleta de cartões: {response.status_code}")
                logger.error(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na requisição de cartões: {e}")
            return None
    
    def collect_comprehensive_data(self) -> bool:
        """Coleta dados abrangentes do Portal da Transparência."""
        logger.info("🏛️ INICIANDO COLETA COMPLETA DE DADOS REAIS")
        logger.info("🎯 Fonte: Portal da Transparência - API Oficial")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Coletar órgãos SIAFI
        logger.info("\n📋 FASE 1: Coletando órgãos SIAFI")
        orgaos = self.get_orgaos_siafi()
        
        if not orgaos:
            logger.error("❌ Falha ao coletar órgãos")
            return False
        
        # Salvar órgãos
        orgaos_file = self.raw_dir / f"orgaos_siafi_real_{timestamp}.json"
        with open(orgaos_file, 'w', encoding='utf-8') as f:
            json.dump(orgaos, f, indent=2, ensure_ascii=False)
        
        # Converter para CSV
        orgaos_csv = self.raw_dir / f"orgaos_siafi_real_{timestamp}.csv"
        df_orgaos = pd.DataFrame(orgaos)
        df_orgaos.to_csv(orgaos_csv, index=False, encoding='utf-8')
        
        logger.info(f"💾 Órgãos salvos: {orgaos_csv.name}")
        
        # 2. Coletar dados de cartões para órgãos principais
        logger.info("\n💳 FASE 2: Coletando dados de cartões de pagamento")
        
        # Filtrar órgãos válidos (não CODIGO INVALIDO)
        orgaos_validos = [o for o in orgaos if 'CODIGO INVALIDO' not in o.get('descricao', '')]
        logger.info(f"📊 {len(orgaos_validos)} órgãos válidos encontrados")
        
        all_cartoes = []
        mes_ano = "01/2024"  # Janeiro 2024
        
        for i, orgao in enumerate(orgaos_validos[:5], 1):  # Primeiros 5 órgãos
            codigo = orgao['codigo']
            nome = orgao['descricao']
            
            logger.info(f"🏛️ ({i}/5) Processando: {codigo} - {nome}")
            
            # Coletar até 3 páginas por órgão
            orgao_cartoes = []
            for pagina in range(1, 4):
                cartoes = self.get_cartoes_pagamento(codigo, mes_ano, pagina)
                
                if cartoes is None:
                    break
                elif len(cartoes) == 0:
                    break
                else:
                    # Adicionar info do órgão aos registros
                    for cartao in cartoes:
                        cartao['orgao_codigo'] = codigo
                        cartao['orgao_nome'] = nome
                    
                    orgao_cartoes.extend(cartoes)
                    
                    if len(cartoes) < 500:  # Última página
                        break
                
                time.sleep(1)  # Rate limiting
            
            if orgao_cartoes:
                logger.info(f"✅ {len(orgao_cartoes)} registros coletados para {nome}")
                all_cartoes.extend(orgao_cartoes)
            else:
                logger.info(f"📄 Sem dados de cartões para {nome}")
            
            time.sleep(2)  # Rate limiting entre órgãos
        
        # 3. Salvar dados de cartões
        if all_cartoes:
            # JSON
            cartoes_json = self.raw_dir / f"cartoes_pagamento_real_{timestamp}.json"
            with open(cartoes_json, 'w', encoding='utf-8') as f:
                json.dump(all_cartoes, f, indent=2, ensure_ascii=False)
            
            # CSV
            cartoes_csv = self.raw_dir / f"cartoes_pagamento_real_{timestamp}.csv"
            df_cartoes = pd.DataFrame(all_cartoes)
            df_cartoes.to_csv(cartoes_csv, index=False, encoding='utf-8')
            
            logger.info(f"💾 Cartões salvos: {cartoes_csv.name}")
            logger.info(f"📊 Total de registros de cartões: {len(all_cartoes):,}")
            
            # 4. Gerar relatórios
            self.generate_comprehensive_report(orgaos_csv, cartoes_csv, orgaos, all_cartoes)
            
            return True
        else:
            logger.warning("⚠️ Nenhum dado de cartão foi coletado")
            return False
    
    def generate_comprehensive_report(self, orgaos_file: Path, cartoes_file: Path, 
                                    orgaos: List[Dict], cartoes: List[Dict]):
        """Gera relatório abrangente da coleta."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"relatorio_coleta_completa_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO COMPLETO - DADOS REAIS DO PORTAL DA TRANSPARÊNCIA\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"🕒 Data da Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"🌐 Fonte: Portal da Transparência - API Oficial\n")
            f.write(f"🔑 Status da API: Autenticada e funcional\n")
            f.write(f"📅 Período dos Dados: Janeiro/2024\n\n")
            
            f.write("📊 DADOS COLETADOS:\n")
            f.write("-" * 50 + "\n")
            f.write(f"🏛️ Órgãos SIAFI: {len(orgaos)} registros\n")
            f.write(f"💳 Cartões de Pagamento: {len(cartoes):,} registros\n")
            f.write(f"📁 Arquivo Órgãos: {orgaos_file.name}\n")
            f.write(f"📁 Arquivo Cartões: {cartoes_file.name}\n\n")
            
            if orgaos:
                f.write("🏛️ ÓRGÃOS VÁLIDOS PROCESSADOS:\n")
                f.write("-" * 50 + "\n")
                orgaos_validos = [o for o in orgaos if 'CODIGO INVALIDO' not in o.get('descricao', '')]
                for i, orgao in enumerate(orgaos_validos[:10], 1):
                    f.write(f"{i:2d}. {orgao['codigo']} - {orgao['descricao']}\n")
                
                if len(orgaos_validos) > 10:
                    f.write(f"... e mais {len(orgaos_validos)-10} órgãos\n")
            
            if cartoes:
                df_cartoes = pd.DataFrame(cartoes)
                
                f.write(f"\n💳 ANÁLISE DOS CARTÕES DE PAGAMENTO:\n")
                f.write("-" * 50 + "\n")
                f.write(f"📋 Total de registros: {len(cartoes):,}\n")
                f.write(f"🗂️ Colunas disponíveis: {len(df_cartoes.columns)}\n")
                
                # Análise de valores
                valor_cols = [col for col in df_cartoes.columns if 'valor' in col.lower()]
                if valor_cols:
                    col_valor = valor_cols[0]
                    try:
                        valores = pd.to_numeric(df_cartoes[col_valor], errors='coerce')
                        f.write(f"\n💰 ANÁLISE FINANCEIRA:\n")
                        f.write(f"💵 Valor total: R$ {valores.sum():,.2f}\n")
                        f.write(f"📊 Valor médio: R$ {valores.mean():,.2f}\n")
                        f.write(f"📈 Valor máximo: R$ {valores.max():,.2f}\n")
                        f.write(f"📉 Valor mínimo: R$ {valores.min():,.2f}\n")
                    except:
                        f.write(f"💰 Coluna de valor: {col_valor} (análise não disponível)\n")
                
                # Órgãos com mais gastos
                if 'orgao_nome' in df_cartoes.columns and valor_cols:
                    try:
                        gastos_por_orgao = df_cartoes.groupby('orgao_nome')[valor_cols[0]].sum().sort_values(ascending=False)
                        f.write(f"\n🏆 TOP 5 ÓRGÃOS POR GASTOS:\n")
                        for i, (orgao, valor) in enumerate(gastos_por_orgao.head().items(), 1):
                            f.write(f"{i}. {orgao}: R$ {valor:,.2f}\n")
                    except:
                        pass
                
                f.write(f"\n📋 ESTRUTURA DOS DADOS:\n")
                f.write("-" * 50 + "\n")
                for i, col in enumerate(df_cartoes.columns, 1):
                    f.write(f"{i:2d}. {col}\n")
                
                f.write(f"\n📄 AMOSTRA DOS DADOS (primeiros 3 registros):\n")
                f.write("-" * 50 + "\n")
                for i, (_, row) in enumerate(df_cartoes.head(3).iterrows()):
                    f.write(f"\n🔹 Registro {i+1}:\n")
                    for col, val in row.items():
                        f.write(f"   {col}: {val}\n")
            
            f.write(f"\n✅ COLETA COMPLETA REALIZADA COM SUCESSO!\n")
            f.write(f"🎯 Dados reais e oficiais do governo federal coletados.\n")
            f.write(f"📡 API do Portal da Transparência totalmente funcional.\n")
            f.write(f"🚀 Sistema pronto para análises avançadas.\n")
        
        logger.info(f"📋 Relatório completo salvo: {report_file.name}")

def main():
    """Função principal."""
    print("🏛️ Gov-Hub - Coletor de Dados Reais do Portal da Transparência")
    print("=" * 70)
    
    collector = TransparenciaRealCollector()
    
    try:
        success = collector.collect_comprehensive_data()
        
        if success:
            print(f"\n🎉 COLETA COMPLETA REALIZADA COM SUCESSO!")
            print(f"📁 Dados salvos em: data/poc_siafi/dados_brutos/")
            print(f"📋 Relatórios em: data/poc_siafi/relatorios/")
            print(f"✅ Dados reais do governo federal coletados e organizados!")
        else:
            print(f"\n❌ FALHA NA COLETA")
            print(f"🔧 Verifique os logs para mais detalhes")
            
    except Exception as e:
        logger.error(f"❌ Erro na execução: {e}")
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()
