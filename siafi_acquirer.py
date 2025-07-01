#!/usr/bin/env python3
"""
Gov-Hub SIAFI Data Acquirer - PoC Focada
Sistema especializado para aquisição e processamento de dados do SIAFI.

Esta versão é 100% focada no SIAFI, removendo complexidade desnecessária
e organizando os resultados de forma clara e estruturada.

Características:
- Download exclusivo de dados do SIAFI
- Organização automática em estrutura clara
- Nomenclatura descritiva para todos os arquivos
- Relatórios específicos para análise do SIAFI
"""

import argparse
import json
import logging
import ssl
import time
import zipfile
import requests
from datetime import datetime
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

# Configuração de SSL para evitar erros de certificado
ssl._create_default_https_context = ssl._create_unverified_context

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data/poc_siafi/relatorios/siafi_acquisition.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


class SiafiDataAcquirer:
    """
    Classe especializada para aquisição de dados do SIAFI.
    """

    def __init__(self):
        """Inicializa o Data Acquirer especializado no SIAFI."""
        self.base_dir = Path("data/poc_siafi")
        self.raw_dir = self.base_dir / "dados_brutos"
        self.processed_dir = self.base_dir / "dados_processados"
        self.reports_dir = self.base_dir / "relatorios"
        self.temp_dir = Path("data/temp")
        
        # Criar diretórios se não existirem
        for dir_path in [self.raw_dir, self.processed_dir, self.reports_dir, self.temp_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("🏛️ SIAFI Data Acquirer inicializado")
        logger.info(f"📁 Dados brutos: {self.raw_dir}")
        logger.info(f"📊 Dados processados: {self.processed_dir}")
        logger.info(f"📋 Relatórios: {self.reports_dir}")

    def download_siafi_data(self) -> bool:
        """
        Baixa dados reais do SIAFI do Portal da Transparência.
        
        Returns:
            bool: True se o download foi bem-sucedido
        """
        logger.info("🚀 === INICIANDO DOWNLOAD DOS DADOS DO SIAFI ===")
        
        # URL do Portal da Transparência para despesas
        current_month = datetime.now().strftime("%Y%m")
        url = f"https://portaldatransparencia.gov.br/download-de-dados/despesas-execucao/{current_month}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        try:
            logger.info(f"📡 Conectando ao Portal da Transparência...")
            logger.info(f"🔗 URL: {url}")
            
            response = requests.get(url, headers=headers, timeout=120, verify=False)
            response.raise_for_status()
            
            # Nome do arquivo mais descritivo
            timestamp = datetime.now().strftime("%Y-%m-%d")
            zip_filename = f"siafi_despesas_execucao_{current_month}_{timestamp}.zip"
            zip_path = self.temp_dir / zip_filename
            
            logger.info(f"💾 Salvando arquivo: {zip_filename}")
            logger.info(f"📦 Tamanho: {len(response.content) / 1024 / 1024:.2f} MB")
            
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extrair e organizar o CSV
            return self._extract_and_organize_csv(zip_path, current_month, timestamp)
            
        except Exception as e:
            logger.error(f"❌ Erro no download do SIAFI: {e}")
            return False

    def _extract_and_organize_csv(self, zip_path: Path, month: str, timestamp: str) -> bool:
        """
        Extrai o CSV do ZIP e organiza com nome descritivo.
        
        Args:
            zip_path: Caminho para o arquivo ZIP
            month: Mês dos dados (YYYYMM)
            timestamp: Timestamp para identificação
            
        Returns:
            bool: True se a extração foi bem-sucedida
        """
        try:
            logger.info(f"📂 Extraindo arquivo ZIP: {zip_path.name}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                logger.info(f"📄 Arquivos no ZIP: {file_list}")
                
                # Encontrar o arquivo CSV principal
                csv_files = [f for f in file_list if f.endswith('.csv')]
                if not csv_files:
                    logger.error("❌ Nenhum arquivo CSV encontrado no ZIP")
                    return False
                
                main_csv = csv_files[0]  # Pegar o primeiro CSV
                
                # Nome descritivo para o arquivo final
                final_csv_name = f"siafi_despesas_execucao_{month}_{timestamp}.csv"
                final_csv_path = self.raw_dir / final_csv_name
                
                # Extrair o arquivo
                with zip_ref.open(main_csv) as source, open(final_csv_path, 'wb') as target:
                    target.write(source.read())
                
                logger.info(f"✅ Arquivo extraído: {final_csv_name}")
                logger.info(f"📊 Tamanho: {final_csv_path.stat().st_size / 1024 / 1024:.2f} MB")
                
                # Contar registros
                line_count = self._count_csv_lines(final_csv_path)
                logger.info(f"📈 Total de registros: {line_count - 1:,} (excluindo cabeçalho)")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro na extração: {e}")
            return False

    def _count_csv_lines(self, csv_path: Path) -> int:
        """Conta o número de linhas no arquivo CSV."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(csv_path, 'r', encoding=encoding) as f:
                    return sum(1 for _ in f)
            except UnicodeDecodeError:
                continue
        
        logger.warning(f"⚠️ Não foi possível contar linhas do arquivo {csv_path.name}")
        return 0

    def process_siafi_data(self) -> bool:
        """
        Processa os dados do SIAFI e gera análises básicas.
        
        Returns:
            bool: True se o processamento foi bem-sucedido
        """
        logger.info("🔄 === INICIANDO PROCESSAMENTO DOS DADOS ===")
        
        # Encontrar o arquivo mais recente
        csv_files = list(self.raw_dir.glob("siafi_despesas_*.csv"))
        if not csv_files:
            logger.error("❌ Nenhum arquivo de dados do SIAFI encontrado")
            return False
        
        latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
        logger.info(f"📊 Processando arquivo: {latest_file.name}")
        
        try:
            # Análise básica do arquivo
            analysis = self._analyze_siafi_file(latest_file)
            
            # Gerar relatório de análise
            self._generate_analysis_report(analysis, latest_file)
            
            # Criar amostra para análise
            self._create_sample_data(latest_file)
            
            logger.info("✅ Processamento concluído com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento: {e}")
            return False

    def _analyze_siafi_file(self, csv_path: Path) -> Dict:
        """Analisa o arquivo do SIAFI e extrai estatísticas básicas."""
        logger.info("📊 Analisando estrutura e conteúdo do arquivo...")
        
        analysis = {
            "arquivo": csv_path.name,
            "tamanho_mb": csv_path.stat().st_size / 1024 / 1024,
            "timestamp_processamento": datetime.now().isoformat(),
        }
        
        try:
            # Ler apenas as primeiras linhas para análise da estrutura
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            file_content = None
            used_encoding = None
            
            for encoding in encodings:
                try:
                    with open(csv_path, 'r', encoding=encoding) as f:
                        first_line = f.readline().strip()
                        analysis["colunas"] = first_line.split(';')
                        analysis["total_colunas"] = len(analysis["colunas"])
                        used_encoding = encoding
                        break
                except UnicodeDecodeError:
                    continue
            
            if used_encoding:
                logger.info(f"📝 Encoding utilizado: {used_encoding}")
                # Contar linhas totais
                with open(csv_path, 'r', encoding=used_encoding) as f:
                    analysis["total_linhas"] = sum(1 for _ in f)
                    analysis["total_registros"] = analysis["total_linhas"] - 1
            else:
                raise Exception("Não foi possível decodificar o arquivo com nenhum encoding testado")
                
                # Ler uma amostra para análise de valores
                sample_data = []
                if used_encoding:
                    with open(csv_path, 'r', encoding=used_encoding) as f:
                        lines = f.readlines()
                        header = lines[0].strip().split(';')
                        
                        # Pegar até 100 linhas de exemplo
                        for i in range(1, min(101, len(lines))):
                            row_data = lines[i].strip().split(';')
                            if len(row_data) == len(header):
                                sample_data.append(dict(zip(header, row_data)))
                
                # Analisar valores monetários
                analysis["analise_valores"] = self._analyze_monetary_values(sample_data)
                
                # Analisar órgãos mais frequentes
                analysis["orgaos_frequentes"] = self._analyze_frequent_organs(sample_data)
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise detalhada: {e}")
            analysis["erro_analise"] = str(e)
        
        return analysis

    def _analyze_monetary_values(self, sample_data: list) -> Dict:
        """Analisa os valores monetários na amostra."""
        valores_empenhados = []
        valores_liquidados = []
        valores_pagos = []
        
        for row in sample_data:
            try:
                # Limpar e converter valores monetários
                emp = row.get('"Valor Empenhado (R$)"', '0').replace('"', '').replace(',', '.')
                liq = row.get('"Valor Liquidado (R$)"', '0').replace('"', '').replace(',', '.')
                pag = row.get('"Valor Pago (R$)"', '0').replace('"', '').replace(',', '.')
                
                if emp and emp != '0':
                    valores_empenhados.append(float(emp))
                if liq and liq != '0':
                    valores_liquidados.append(float(liq))
                if pag and pag != '0':
                    valores_pagos.append(float(pag))
                    
            except (ValueError, KeyError):
                continue
        
        return {
            "empenhado": {
                "total_registros": len(valores_empenhados),
                "soma": sum(valores_empenhados),
                "media": sum(valores_empenhados) / len(valores_empenhados) if valores_empenhados else 0,
                "maximo": max(valores_empenhados) if valores_empenhados else 0
            },
            "liquidado": {
                "total_registros": len(valores_liquidados),
                "soma": sum(valores_liquidados),
                "media": sum(valores_liquidados) / len(valores_liquidados) if valores_liquidados else 0
            },
            "pago": {
                "total_registros": len(valores_pagos),
                "soma": sum(valores_pagos),
                "media": sum(valores_pagos) / len(valores_pagos) if valores_pagos else 0
            }
        }

    def _analyze_frequent_organs(self, sample_data: list) -> Dict:
        """Analisa os órgãos mais frequentes na amostra."""
        organs = {}
        
        for row in sample_data:
            try:
                organ_name = row.get('"Nome Órgão Superior"', '').replace('"', '').strip()
                if organ_name and organ_name != 'Sem informação':
                    organs[organ_name] = organs.get(organ_name, 0) + 1
            except KeyError:
                continue
        
        # Retornar os 10 mais frequentes
        sorted_organs = sorted(organs.items(), key=lambda x: x[1], reverse=True)[:10]
        return dict(sorted_organs)

    def _generate_analysis_report(self, analysis: Dict, csv_path: Path):
        """Gera um relatório detalhado da análise."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = self.reports_dir / f"siafi_analise_detalhada_{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE ANÁLISE - DADOS DO SIAFI\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Arquivo Analisado: {analysis['arquivo']}\n")
            f.write(f"Tamanho: {analysis['tamanho_mb']:.2f} MB\n")
            f.write(f"Data do Processamento: {analysis['timestamp_processamento']}\n\n")
            
            f.write("ESTRUTURA DO ARQUIVO:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Colunas: {analysis['total_colunas']}\n")
            f.write(f"Total de Linhas: {analysis['total_linhas']:,}\n")
            f.write(f"Total de Registros: {analysis['total_registros']:,}\n\n")
            
            if 'analise_valores' in analysis:
                f.write("ANÁLISE DE VALORES MONETÁRIOS:\n")
                f.write("-" * 40 + "\n")
                valores = analysis['analise_valores']
                
                f.write(f"VALORES EMPENHADOS:\n")
                f.write(f"  Registros com valores: {valores['empenhado']['total_registros']:,}\n")
                f.write(f"  Soma total: R$ {valores['empenhado']['soma']:,.2f}\n")
                f.write(f"  Valor médio: R$ {valores['empenhado']['media']:,.2f}\n")
                f.write(f"  Maior valor: R$ {valores['empenhado']['maximo']:,.2f}\n\n")
                
                f.write(f"VALORES LIQUIDADOS:\n")
                f.write(f"  Registros com valores: {valores['liquidado']['total_registros']:,}\n")
                f.write(f"  Soma total: R$ {valores['liquidado']['soma']:,.2f}\n\n")
                
                f.write(f"VALORES PAGOS:\n")
                f.write(f"  Registros com valores: {valores['pago']['total_registros']:,}\n")
                f.write(f"  Soma total: R$ {valores['pago']['soma']:,.2f}\n\n")
            
            if 'orgaos_frequentes' in analysis:
                f.write("ÓRGÃOS MAIS FREQUENTES (TOP 10):\n")
                f.write("-" * 40 + "\n")
                for i, (organ, count) in enumerate(analysis['orgaos_frequentes'].items(), 1):
                    f.write(f"{i:2d}. {organ}: {count} registros\n")
                f.write("\n")
            
            f.write("ESTRUTURA DE COLUNAS:\n")
            f.write("-" * 40 + "\n")
            for i, col in enumerate(analysis['colunas'], 1):
                clean_col = col.replace('"', '').strip()
                f.write(f"{i:2d}. {clean_col}\n")
        
        logger.info(f"📋 Relatório de análise salvo: {report_path.name}")

    def _create_sample_data(self, csv_path: Path):
        """Cria uma amostra dos dados para análise rápida."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        sample_path = self.processed_dir / f"siafi_amostra_1000_registros_{timestamp}.csv"
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as source:
                lines = source.readlines()
                
                # Pegar cabeçalho + primeiros 1000 registros
                sample_lines = lines[:1001] if len(lines) > 1001 else lines
                
                with open(sample_path, 'w', encoding='utf-8') as target:
                    target.writelines(sample_lines)
            
            logger.info(f"📊 Amostra criada: {sample_path.name} ({len(sample_lines)-1} registros)")
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao criar amostra: {e}")

    def generate_final_report(self):
        """Gera um relatório final consolidado da PoC."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = self.reports_dir / f"relatorio_final_poc_siafi_{timestamp}.txt"
        
        # Coletar informações dos arquivos gerados
        raw_files = list(self.raw_dir.glob("*.csv"))
        processed_files = list(self.processed_dir.glob("*.csv"))
        report_files = list(self.reports_dir.glob("*.txt"))
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO FINAL - POC SIAFI GOV-HUB\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Data de Execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Foco: Sistema Integrado de Administração Financeira (SIAFI)\n\n")
            
            f.write("RESUMO DA EXECUÇÃO:\n")
            f.write("-" * 40 + "\n")
            f.write("✅ Download de dados reais do SIAFI realizado\n")
            f.write("✅ Processamento e análise concluídos\n")
            f.write("✅ Organização de arquivos finalizada\n")
            f.write("✅ Relatórios gerados com sucesso\n\n")
            
            f.write("ARQUIVOS GERADOS:\n")
            f.write("-" * 40 + "\n")
            
            f.write("📁 DADOS BRUTOS:\n")
            for file in raw_files:
                size_mb = file.stat().st_size / 1024 / 1024
                f.write(f"   📄 {file.name} ({size_mb:.2f} MB)\n")
            
            f.write("\n📁 DADOS PROCESSADOS:\n")
            for file in processed_files:
                size_kb = file.stat().st_size / 1024
                f.write(f"   📊 {file.name} ({size_kb:.1f} KB)\n")
            
            f.write("\n📁 RELATÓRIOS:\n")
            for file in report_files:
                size_kb = file.stat().st_size / 1024
                f.write(f"   📋 {file.name} ({size_kb:.1f} KB)\n")
            
            f.write("\nESTATÍSTICAS:\n")
            f.write("-" * 40 + "\n")
            if raw_files:
                latest_raw = max(raw_files, key=lambda x: x.stat().st_mtime)
                line_count = self._count_csv_lines(latest_raw)
                f.write(f"Total de registros SIAFI: {line_count-1:,}\n")
                f.write(f"Tamanho do dataset: {latest_raw.stat().st_size / 1024 / 1024:.2f} MB\n")
            
            f.write(f"\nStatus: ✅ POC CONCLUÍDA COM SUCESSO!\n")
        
        logger.info(f"📋 Relatório final salvo: {report_path.name}")

    def run_complete_poc(self):
        """Executa a PoC completa do SIAFI."""
        logger.info("🚀 === INICIANDO POC COMPLETA DO SIAFI ===")
        
        # Passo 1: Download dos dados
        if not self.download_siafi_data():
            logger.error("❌ Falha no download dos dados. Encerrando PoC.")
            return False
        
        # Passo 2: Processamento e análise
        if not self.process_siafi_data():
            logger.error("❌ Falha no processamento dos dados. Encerrando PoC.")
            return False
        
        # Passo 3: Relatório final
        self.generate_final_report()
        
        logger.info("🎉 === POC DO SIAFI CONCLUÍDA COM SUCESSO! ===")
        return True


def main():
    parser = argparse.ArgumentParser(description="Gov-Hub SIAFI Data Acquirer")
    parser.add_argument("--verbose", action="store_true", help="Ativar modo verbose")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    acquirer = SiafiDataAcquirer()
    success = acquirer.run_complete_poc()
    
    if success:
        print("\n🎉 PoC do SIAFI executada com sucesso!")
        print("📁 Verifique a pasta 'data/poc_siafi' para os resultados")
    else:
        print("\n❌ PoC falhou. Verifique os logs para detalhes.")


if __name__ == "__main__":
    main()
