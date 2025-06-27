#!/usr/bin/env python3
"""
Gov-Hub Data Processor Module
Módulo para processamento avançado de dados SIAFI em larga escala.

Este módulo contém processadores especializados para diferentes tipos de arquivos
governamentais, com foco em arquivos SIAFI grandes.

Classes:
    SiafiLargeFileProcessor: Processador especializado para arquivos SIAFI grandes
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SiafiLargeFileProcessor:
    """
    Processador especializado para arquivos SIAFI grandes.
    
    Handles large SIAFI files with different encoding and parsing configurations.
    """
    
    def __init__(self, raw_data_dir: str = "data/raw", processed_data_dir: str = "data/processed"):
        """
        Inicializa o processador de arquivos SIAFI.

        Args:
            raw_data_dir: Diretório com dados brutos
            processed_data_dir: Diretório para dados processados
        """
        self.raw_dir = Path(raw_data_dir)
        self.processed_dir = Path(processed_data_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações de parsing para diferentes encodings
        self.parsing_configs = [
            {"sep": ";", "encoding": "utf-8", "quotechar": '"'},
            {"sep": ";", "encoding": "latin-1", "quotechar": '"'},
            {"sep": ";", "encoding": "cp1252", "quotechar": '"'},
            {"sep": ";", "encoding": "utf-8", "quotechar": '"', "quoting": 1},  # QUOTE_ALL
        ]
        
        logger.info("SiafiLargeFileProcessor inicializado")
        logger.info(f"Diretório de dados brutos: {self.raw_dir}")
        logger.info(f"Diretório de dados processados: {self.processed_dir}")
    
    def analyze_file_structure(self, filepath: Path) -> Optional[str]:
        """
        Analisa a estrutura do arquivo para detectar o separador correto.
        
        Args:
            filepath: Caminho para o arquivo SIAFI
            
        Returns:
            Separador provável ou None se falhar
        """
        logger.info(f"🔍 Analisando estrutura do arquivo: {filepath.name}")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                # Ler primeiras linhas
                lines = []
                for i in range(5):
                    line = f.readline().strip()
                    if not line:
                        break
                    lines.append(line)
                    logger.debug(f"Linha {i+1}: {line[:100]}...")
                
                if not lines:
                    logger.error("Arquivo vazio ou ilegível")
                    return None
                
                # Analisar delimitadores na primeira linha (header)
                header = lines[0]
                semicolon_count = header.count(";")
                comma_count = header.count(",")
                quote_count = header.count('"')
                
                logger.info(f"Análise de delimitadores:")
                logger.info(f"  ; (ponto-vírgula): {semicolon_count}")
                logger.info(f"  , (vírgula): {comma_count}")
                logger.info(f'  " (aspas): {quote_count}')
                
                # Detectar provável separador
                probable_sep = ";" if semicolon_count > comma_count else ","
                logger.info(f"🎯 Separador provável: '{probable_sep}'")
                
                return probable_sep
                
        except Exception as e:
            logger.error(f"Erro na análise da estrutura: {e}")
            return None
    
    def process_large_siafi_file(self, filepath: Path, max_rows: int = 5000) -> Optional[pd.DataFrame]:
        """
        Processa arquivo SIAFI grande com tratamento robusto de encoding e parsing.
        
        Args:
            filepath: Caminho para o arquivo SIAFI
            max_rows: Número máximo de registros a processar
            
        Returns:
            DataFrame processado ou None se falhar
        """
        if not filepath.exists():
            logger.error(f"Arquivo não encontrado: {filepath}")
            return None
        
        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        logger.info(f"📄 Processando arquivo SIAFI: {filepath.name}")
        logger.info(f"📏 Tamanho: {file_size_mb:.1f} MB")
        
        # Tentar diferentes configurações de parsing
        for i, config in enumerate(self.parsing_configs, 1):
            try:
                logger.info(f"🔄 Tentativa {i}: {config}")
                
                # Teste com amostra pequena primeiro
                df_sample = pd.read_csv(filepath, nrows=10, **config)
                logger.info(f"✅ Configuração {i} funcionou!")
                logger.info(f"📊 Colunas encontradas: {len(df_sample.columns)}")
                logger.info(f"📋 Primeiras colunas: {list(df_sample.columns)[:3]}")
                
                # Se funcionou com sample, carregar arquivo com limite
                logger.info(f"📥 Carregando arquivo completo (primeiros {max_rows} registros)...")
                df_full = pd.read_csv(filepath, nrows=max_rows, **config)
                
                logger.info(f"✅ Sucesso! Carregados {len(df_full)} registros")
                
                # Executar análise dos dados
                self._analyze_dataframe(df_full)
                
                # Salvar amostra processada
                output_filename = f"siafi_real_sample_{max_rows}.csv"
                output_path = self.processed_dir / output_filename
                df_full.to_csv(output_path, index=False, encoding="utf-8")
                logger.info(f"✅ Amostra salva: {output_path}")
                
                return df_full
                
            except Exception as e:
                logger.warning(f"❌ Configuração {i} falhou: {e}")
                continue
        
        logger.error("❌ Todas as configurações de parsing falharam")
        return None
    
    def _analyze_dataframe(self, df: pd.DataFrame) -> None:
        """
        Executa análise estatística básica do DataFrame SIAFI.
        
        Args:
            df: DataFrame a ser analisado
        """
        logger.info("\n📊 === ANÁLISE DOS DADOS SIAFI ===")
        logger.info(f"   📋 Colunas: {len(df.columns)}")
        logger.info(f"   📄 Registros: {len(df)}")
        
        # Identificar colunas de valor
        value_cols = [col for col in df.columns if "valor" in col.lower()]
        logger.info(f"   💰 Colunas de valor: {value_cols}")
        
        # Calcular estatísticas básicas para colunas de valor
        for col in value_cols:
            try:
                # Limpar e converter valores
                values = (
                    df[col]
                    .astype(str)
                    .str.replace(",", ".")
                    .str.replace('"', "")
                )
                values = pd.to_numeric(values, errors="coerce")
                total = values.sum()
                count = values.count()
                logger.info(f"   💵 {col}: {count} valores, Total: R$ {total:,.2f}")
            except Exception as e:
                logger.warning(f"   ⚠️ Erro ao processar coluna {col}: {e}")
    
    def find_and_process_siafi_files(self) -> List[pd.DataFrame]:
        """
        Encontra e processa todos os arquivos SIAFI no diretório.
        
        Returns:
            Lista de DataFrames processados
        """
        logger.info("🔍 Procurando arquivos SIAFI...")
        
        # Padrões de arquivos SIAFI
        siafi_patterns = ["*siafi*.csv", "*Despesas*.csv", "*202501*.csv"]
        
        siafi_files = []
        for pattern in siafi_patterns:
            siafi_files.extend(self.raw_dir.glob(pattern))
        
        if not siafi_files:
            logger.warning("Nenhum arquivo SIAFI encontrado")
            return []
        
        logger.info(f"📁 Encontrados {len(siafi_files)} arquivo(s) SIAFI:")
        for file in siafi_files:
            logger.info(f"   - {file.name}")
        
        processed_dataframes = []
        for file in siafi_files:
            # Análise da estrutura
            separator = self.analyze_file_structure(file)
            
            # Processamento dos dados
            df = self.process_large_siafi_file(file)
            if df is not None:
                processed_dataframes.append(df)
        
        return processed_dataframes


def main():
    """Função principal para execução standalone."""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
    )
    
    logger.info("🚀 === Processador Especializado SIAFI ===")
    
    try:
        processor = SiafiLargeFileProcessor()
        dataframes = processor.find_and_process_siafi_files()
        
        if dataframes:
            logger.info(f"🎉 === PROCESSAMENTO CONCLUÍDO: {len(dataframes)} arquivo(s) ===")
            return 0
        else:
            logger.error("❌ === FALHA NO PROCESSAMENTO ===")
            return 1
            
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
