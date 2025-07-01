#!/usr/bin/env python3
"""
Organizador de Dados SIAFI - PoC Focada
Script para organizar os dados existentes do SIAFI na nova estrutura.
"""

import shutil
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def organize_existing_siafi_data():
    """Organiza os dados existentes do SIAFI na nova estrutura."""
    
    # Diretórios
    base_dir = Path("data/poc_siafi")
    raw_dir = base_dir / "dados_brutos"
    processed_dir = base_dir / "dados_processados"
    reports_dir = base_dir / "relatorios"
    
    # Criar diretórios
    for dir_path in [raw_dir, processed_dir, reports_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    logger.info("🏛️ Organizando dados existentes do SIAFI...")
    
    # Organizar arquivos do SIAFI disponíveis
    siafi_files = [
        Path("data/raw/siafi_2025-06-25.csv"),
        Path("data/raw/siafi_sample.csv")
    ]
    
    organized_files = []
    for source_file in siafi_files:
        if source_file.exists():
            dest_file = raw_dir / f"siafi_dados_{source_file.stem}_organizado.csv"
            if not dest_file.exists():
                shutil.copy2(source_file, dest_file)
                logger.info(f"📄 Copiado: {dest_file.name}")
                organized_files.append(dest_file)
            else:
                organized_files.append(dest_file)
    
    # Processar cada arquivo organizado
    for file in organized_files:
        # Criar amostra para análise
        create_sample(file, processed_dir)
        
        # Gerar relatório básico
        generate_basic_report(file, reports_dir)
    
    # Criar relatório final
    generate_final_organized_report(base_dir)
    
    logger.info("✅ Organização concluída!")

def create_sample(source_file: Path, processed_dir: Path):
    """Cria uma amostra dos dados para análise."""
    try:
        sample_file = processed_dir / "siafi_amostra_1000_registros_2025-06-30.csv"
        
        # Tentar diferentes encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
        
        for encoding in encodings:
            try:
                with open(source_file, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    
                    # Pegar cabeçalho + primeiros 1000 registros
                    sample_lines = lines[:1001] if len(lines) > 1001 else lines
                    
                    with open(sample_file, 'w', encoding='utf-8') as target:
                        target.writelines(sample_lines)
                    
                    logger.info(f"📊 Amostra criada: {sample_file.name} ({len(sample_lines)-1} registros)")
                    break
                    
            except UnicodeDecodeError:
                continue
                
    except Exception as e:
        logger.warning(f"⚠️ Erro ao criar amostra: {e}")

def generate_basic_report(source_file: Path, reports_dir: Path):
    """Gera um relatório básico do arquivo."""
    report_file = reports_dir / "siafi_relatorio_basico_2025-06-30.txt"
    
    file_size_mb = source_file.stat().st_size / 1024 / 1024
    
    # Contar linhas com encoding robusto
    line_count = 0
    columns = []
    
    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    
    for encoding in encodings:
        try:
            with open(source_file, 'r', encoding=encoding) as f:
                lines = f.readlines()
                line_count = len(lines)
                if lines:
                    columns = lines[0].strip().split(';')
                break
        except UnicodeDecodeError:
            continue
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO BÁSICO - DADOS DO SIAFI\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Arquivo: {source_file.name}\n")
        f.write(f"Tamanho: {file_size_mb:.2f} MB\n")
        f.write(f"Total de linhas: {line_count:,}\n")
        f.write(f"Total de registros: {line_count-1:,} (excluindo cabeçalho)\n")
        f.write(f"Total de colunas: {len(columns)}\n\n")
        
        f.write("ESTRUTURA DE COLUNAS:\n")
        f.write("-" * 40 + "\n")
        for i, col in enumerate(columns[:10], 1):  # Primeiras 10 colunas
            clean_col = col.replace('"', '').strip()
            f.write(f"{i:2d}. {clean_col}\n")
        
        if len(columns) > 10:
            f.write(f"... e mais {len(columns)-10} colunas\n")
    
    logger.info(f"📋 Relatório básico salvo: {report_file.name}")

def generate_final_organized_report(base_dir: Path):
    """Gera relatório final da organização."""
    report_file = base_dir / "relatorios" / "relatorio_final_organizacao_2025-06-30.txt"
    
    raw_files = list((base_dir / "dados_brutos").glob("*.csv"))
    processed_files = list((base_dir / "dados_processados").glob("*.csv"))
    report_files = list((base_dir / "relatorios").glob("*.txt"))
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO FINAL - ORGANIZAÇÃO POC SIAFI\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Data de Organização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("Foco: 100% Sistema Integrado de Administração Financeira (SIAFI)\n\n")
        
        f.write("ESTRUTURA ORGANIZADA:\n")
        f.write("-" * 40 + "\n")
        f.write("📁 data/poc_siafi/\n")
        f.write("   📂 dados_brutos/ - Dados originais do SIAFI\n")
        f.write("   📂 dados_processados/ - Amostras e análises\n")
        f.write("   📂 relatorios/ - Relatórios e logs\n\n")
        
        f.write("ARQUIVOS ORGANIZADOS:\n")
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
            if file.name != report_file.name:  # Não incluir o próprio arquivo
                size_kb = file.stat().st_size / 1024
                f.write(f"   📋 {file.name} ({size_kb:.1f} KB)\n")
        
        f.write("\nESTATÍSTICAS FINAIS:\n")
        f.write("-" * 40 + "\n")
        if raw_files:
            main_file = raw_files[0]
            encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
            line_count = 0
            
            for encoding in encodings:
                try:
                    with open(main_file, 'r', encoding=encoding) as file:
                        line_count = sum(1 for _ in file)
                    break
                except UnicodeDecodeError:
                    continue
            
            f.write(f"📊 Total de registros SIAFI: {line_count-1:,}\n")
            f.write(f"📦 Tamanho do dataset: {main_file.stat().st_size / 1024 / 1024:.2f} MB\n")
            f.write(f"🎯 Fonte: Portal da Transparência (SIAFI)\n")
        
        f.write("\n✅ STATUS: ORGANIZAÇÃO CONCLUÍDA COM SUCESSO!\n")
        f.write("🎯 POC agora focada 100% no SIAFI com estrutura clara e organizada.\n")
    
    logger.info(f"📋 Relatório final de organização salvo: {report_file.name}")

if __name__ == "__main__":
    organize_existing_siafi_data()
