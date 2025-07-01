#!/usr/bin/env python3
"""
Gerador de Dados SIAFI Realistas - Gov-Hub PoC
Script para gerar dados simulados mas realistas do SIAFI para demonstração.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import logging
import random
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SiafiDataGenerator:
    """Gerador de dados realistas do SIAFI para PoC."""
    
    def __init__(self):
        self.base_dir = Path("data/poc_siafi")
        self.raw_dir = self.base_dir / "dados_brutos"
        self.processed_dir = self.base_dir / "dados_processados"
        self.reports_dir = self.base_dir / "relatorios"
        
        # Criar diretórios
        for dir_path in [self.raw_dir, self.processed_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def generate_realistic_siafi_data(self, num_records=5000):
        """
        Gera dados realistas do SIAFI baseados na estrutura real.
        
        Args:
            num_records: Número de registros a gerar
        """
        logger.info(f"🏛️ Gerando {num_records:,} registros realistas do SIAFI...")
        
        # Órgãos do governo federal (códigos reais)
        orgaos = {
            26291: "Ministério da Educação",
            36201: "Ministério da Saúde", 
            39201: "Ministério da Defesa",
            20101: "Presidência da República",
            30101: "Ministério da Justiça e Segurança Pública",
            44101: "Ministério do Desenvolvimento e Assistência Social",
            55101: "Ministério da Infraestrutura",
            25101: "Ministério da Economia"
        }
        
        # Tipos de despesa (funcional)
        funcoes = {
            12: "Educação",
            10: "Saúde",
            2: "Defesa Nacional",
            4: "Administração",
            14: "Direitos da Cidadania",
            26: "Transporte",
            28: "Encargos Especiais",
            6: "Segurança Pública"
        }
        
        # Modalidades de aplicação
        modalidades = {
            90: "Aplicações Diretas",
            41: "Transferências para Estados",
            42: "Transferências para Municípios",
            50: "Transferências para Instituições Privadas"
        }
        
        # Gerar dados
        data = []
        for i in range(num_records):
            orgao_codigo = random.choice(list(orgaos.keys()))
            funcao_codigo = random.choice(list(funcoes.keys()))
            modalidade_codigo = random.choice(list(modalidades.keys()))
            
            # Valores realistas baseados em distribuição real do orçamento
            if orgao_codigo in [26291, 36201]:  # Educação e Saúde - valores maiores
                valor_base = random.uniform(50000, 5000000)
            elif orgao_codigo == 39201:  # Defesa - valores muito altos
                valor_base = random.uniform(100000, 10000000)
            else:
                valor_base = random.uniform(10000, 1000000)
            
            # Data no ano atual
            data_empenho = datetime.now() - timedelta(days=random.randint(0, 365))
            
            registro = {
                "id": f"SIAFI{i+1:06d}",
                "ano_exercicio": data_empenho.year,
                "mes_empenho": data_empenho.month,
                "data_empenho": data_empenho.strftime("%Y-%m-%d"),
                "codigo_orgao": orgao_codigo,
                "nome_orgao": orgaos[orgao_codigo],
                "codigo_funcao": funcao_codigo,
                "nome_funcao": funcoes[funcao_codigo],
                "codigo_modalidade_aplicacao": modalidade_codigo,
                "nome_modalidade_aplicacao": modalidades[modalidade_codigo],
                "numero_empenho": f"{data_empenho.year}NE{random.randint(100000, 999999)}",
                "valor_empenhado": round(valor_base, 2),
                "valor_liquidado": round(valor_base * random.uniform(0.7, 1.0), 2),
                "valor_pago": round(valor_base * random.uniform(0.5, 0.9), 2),
                "codigo_ug": random.randint(100000, 999999),
                "gestao": random.randint(10000, 99999),
                "cnpj_credor": f"{random.randint(10000000, 99999999):08d}{random.randint(1000, 9999):04d}{random.randint(10, 99):02d}",
                "nome_credor": f"Empresa {chr(65 + i % 26)} Ltda" if i % 3 != 0 else f"Universidade {chr(65 + i % 26)}",
                "natureza_juridica": "Empresa Privada" if i % 3 != 0 else "Universidade Pública",
                "elemento_despesa": random.choice(["33903601", "33903014", "44905201", "33903999", "33903093"]),
                "fonte_recursos": random.choice(["0100", "0250", "0259", "0281", "8100"])
            }
            
            data.append(registro)
        
        # Criar DataFrame
        df = pd.DataFrame(data)
        
        # Salvar como CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = self.raw_dir / f"siafi_dados_realistas_{timestamp}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        # Salvar como JSON também
        json_file = self.raw_dir / f"siafi_dados_realistas_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Dados salvos: {csv_file.name}")
        logger.info(f"💾 JSON salvo: {json_file.name}")
        
        # Gerar relatório detalhado
        self.generate_detailed_report(df, csv_file)
        
        # Criar amostra processada
        self.create_processed_sample(df)
        
        return csv_file
    
    def generate_detailed_report(self, df, csv_file):
        """Gera relatório detalhado dos dados gerados."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"relatorio_dados_realistas_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DETALHADO - DADOS SIAFI REALISTAS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Arquivo: {csv_file.name}\n")
            f.write(f"Total de Registros: {len(df):,}\n")
            f.write(f"Tamanho do Arquivo: {csv_file.stat().st_size / 1024 / 1024:.2f} MB\n\n")
            
            f.write("ANÁLISE FINANCEIRA:\n")
            f.write("-" * 40 + "\n")
            f.write(f"💰 Valor Total Empenhado: R$ {df['valor_empenhado'].sum():,.2f}\n")
            f.write(f"💰 Valor Total Liquidado: R$ {df['valor_liquidado'].sum():,.2f}\n")
            f.write(f"💰 Valor Total Pago: R$ {df['valor_pago'].sum():,.2f}\n")
            f.write(f"💰 Valor Médio por Empenho: R$ {df['valor_empenhado'].mean():,.2f}\n")
            f.write(f"💰 Maior Empenho: R$ {df['valor_empenhado'].max():,.2f}\n")
            f.write(f"💰 Menor Empenho: R$ {df['valor_empenhado'].min():,.2f}\n\n")
            
            f.write("ANÁLISE POR ÓRGÃO:\n")
            f.write("-" * 40 + "\n")
            orgao_summary = df.groupby('nome_orgao').agg({
                'valor_empenhado': ['count', 'sum']
            }).round(2)
            
            for orgao in orgao_summary.index:
                count = orgao_summary.loc[orgao, ('valor_empenhado', 'count')]
                total = orgao_summary.loc[orgao, ('valor_empenhado', 'sum')]
                f.write(f"🏛️ {orgao}:\n")
                f.write(f"   📊 {count:,} empenhos | R$ {total:,.2f}\n\n")
            
            f.write("ANÁLISE POR FUNÇÃO:\n")
            f.write("-" * 40 + "\n")
            funcao_summary = df.groupby('nome_funcao').agg({
                'valor_empenhado': ['count', 'sum']
            }).round(2)
            
            for funcao in funcao_summary.index:
                count = funcao_summary.loc[funcao, ('valor_empenhado', 'count')]
                total = funcao_summary.loc[funcao, ('valor_empenhado', 'sum')]
                f.write(f"🎯 {funcao}: {count:,} empenhos | R$ {total:,.2f}\n")
            
            f.write(f"\nDISTRIBUIÇÃO TEMPORAL:\n")
            f.write("-" * 40 + "\n")
            monthly = df.groupby('mes_empenho')['valor_empenhado'].sum()
            for mes, valor in monthly.items():
                f.write(f"📅 Mês {mes:02d}: R$ {valor:,.2f}\n")
            
            f.write(f"\n✅ RELATÓRIO GERADO COM SUCESSO!\n")
            f.write(f"🎯 Dados prontos para análise e demonstração da PoC.\n")
        
        logger.info(f"📋 Relatório detalhado salvo: {report_file.name}")
    
    def create_processed_sample(self, df):
        """Cria amostra processada para análise."""
        # Amostra de 100 registros
        sample = df.head(100).copy()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sample_file = self.processed_dir / f"siafi_amostra_processada_{timestamp}.csv"
        
        sample.to_csv(sample_file, index=False, encoding='utf-8')
        logger.info(f"📊 Amostra processada criada: {sample_file.name}")
        
        # Relatório da amostra
        sample_report = self.processed_dir / f"relatorio_amostra_{timestamp}.txt"
        with open(sample_report, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DA AMOSTRA PROCESSADA\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Registros na amostra: {len(sample)}\n")
            f.write(f"Valor total da amostra: R$ {sample['valor_empenhado'].sum():,.2f}\n")
            f.write(f"Órgãos representados: {sample['nome_orgao'].nunique()}\n")
            f.write(f"Funções representadas: {sample['nome_funcao'].nunique()}\n\n")
            
            f.write("PRIMEIROS 5 REGISTROS:\n")
            f.write("-" * 30 + "\n")
            for i, (_, row) in enumerate(sample.head(5).iterrows()):
                f.write(f"\n{i+1}. {row['numero_empenho']}\n")
                f.write(f"   Órgão: {row['nome_orgao']}\n")
                f.write(f"   Valor: R$ {row['valor_empenhado']:,.2f}\n")
                f.write(f"   Data: {row['data_empenho']}\n")

def main():
    """Função principal."""
    generator = SiafiDataGenerator()
    
    logger.info("🚀 Iniciando geração de dados realistas do SIAFI...")
    
    # Gerar conjunto de dados para demonstração
    arquivo = generator.generate_realistic_siafi_data(num_records=5000)
    
    logger.info(f"✅ Geração concluída! Arquivo: {arquivo.name}")
    logger.info("🎯 Dados realistas prontos para análise da PoC SIAFI!")

if __name__ == "__main__":
    main()
