#!/usr/bin/env python3
"""
Processador especializado para o arquivo SIAFI grande (202501_Despesas_2025-06-26.csv)
"""

import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_large_siafi_file():
    """Processa o arquivo grande do SIAFI com tratamento específico"""

    siafi_file = Path("data/raw/202501_Despesas_2025-06-26.csv")

    if not siafi_file.exists():
        logger.error("Arquivo SIAFI não encontrado")
        return None

    logger.info(f"📄 Processando arquivo SIAFI: {siafi_file}")
    logger.info(f"📏 Tamanho: {siafi_file.stat().st_size / (1024*1024):.1f} MB")

    try:
        # Tentar diferentes configurações de parsing
        configs = [
            {"sep": ";", "encoding": "utf-8", "quotechar": '"'},
            {"sep": ";", "encoding": "latin-1", "quotechar": '"'},
            {"sep": ";", "encoding": "cp1252", "quotechar": '"'},
            {
                "sep": ";",
                "encoding": "utf-8",
                "quotechar": '"',
                "quoting": 1,
            },  # QUOTE_ALL
        ]

        for i, config in enumerate(configs, 1):
            try:
                logger.info(f"🔄 Tentativa {i}: {config}")

                # Ler apenas algumas linhas primeiro para testar
                df_sample = pd.read_csv(siafi_file, nrows=10, **config)
                logger.info(f"✅ Configuração {i} funcionou!")
                logger.info(f"📊 Colunas encontradas: {len(df_sample.columns)}")
                logger.info(f"📋 Primeiras colunas: {list(df_sample.columns)[:3]}")

                # Se funcionou com sample, tentar arquivo completo (com limite)
                logger.info(
                    "📥 Carregando arquivo completo (primeiros 5000 registros)..."
                )
                df_full = pd.read_csv(siafi_file, nrows=5000, **config)

                logger.info(f"✅ Sucesso! Carregados {len(df_full)} registros")

                # Análise básica
                logger.info("\n📊 === ANÁLISE DOS DADOS SIAFI ===")
                logger.info(f"   📋 Colunas: {len(df_full.columns)}")
                logger.info(f"   📄 Registros: {len(df_full)}")

                # Identificar colunas de valor
                value_cols = [col for col in df_full.columns if "valor" in col.lower()]
                logger.info(f"   💰 Colunas de valor: {value_cols}")

                # Calcular estatísticas básicas
                for col in value_cols:
                    try:
                        # Limpar e converter valores
                        values = (
                            df_full[col]
                            .astype(str)
                            .str.replace(",", ".")
                            .str.replace('"', "")
                        )
                        values = pd.to_numeric(values, errors="coerce")
                        total = values.sum()
                        count = values.count()
                        logger.info(
                            f"   💵 {col}: {count} valores, Total: R$ {total:,.2f}"
                        )
                    except Exception:
                        pass

                # Salvar amostra processada
                output_path = Path("data/processed/siafi_real_amostra_5k.csv")
                df_full.to_csv(output_path, index=False, encoding="utf-8")
                logger.info(f"✅ Amostra salva: {output_path}")

                return df_full

            except Exception as e:
                logger.warning(f"❌ Configuração {i} falhou: {e}")
                continue

        logger.error("❌ Todas as configurações de parsing falharam")
        return None

    except Exception as e:
        logger.error(f"❌ Erro geral: {e}")
        return None


def analyze_file_structure():
    """Analisa a estrutura do arquivo manualmente"""

    siafi_file = Path("data/raw/202501_Despesas_2025-06-26.csv")

    logger.info("🔍 === ANÁLISE MANUAL DA ESTRUTURA ===")

    try:
        with open(siafi_file, "r", encoding="utf-8") as f:
            # Ler primeiras linhas
            lines = []
            for i in range(5):
                line = f.readline().strip()
                lines.append(line)
                logger.info(
                    f"   Linha {i+1}: {line[:100]}..."
                    if len(line) > 100
                    else f"   Linha {i+1}: {line}"
                )

            # Contar delimitadores na primeira linha (header)
            header = lines[0]
            semicolon_count = header.count(";")
            comma_count = header.count(",")
            quote_count = header.count('"')

            logger.info("\n📊 Análise de delimitadores:")
            logger.info(f"   ; (ponto-vírgula): {semicolon_count}")
            logger.info(f"   , (vírgula): {comma_count}")
            logger.info(f'   " (aspas): {quote_count}')

            # Detectar provável separador
            probable_sep = ";" if semicolon_count > comma_count else ","
            logger.info(f"   🎯 Separador provável: '{probable_sep}'")

            return probable_sep

    except Exception as e:
        logger.error(f"❌ Erro na análise manual: {e}")
        return None


if __name__ == "__main__":
    logger.info("🚀 === Processador Especializado SIAFI ===")

    # Análise da estrutura
    separator = analyze_file_structure()

    # Processamento dos dados
    df = process_large_siafi_file()

    if df is not None:
        logger.info("🎉 === PROCESSAMENTO SIAFI CONCLUÍDO ===")
    else:
        logger.error("❌ === FALHA NO PROCESSAMENTO ===")
