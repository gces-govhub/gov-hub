#!/usr/bin/env python3
"""
Gov-Hub Advanced Integration Module
Módulo para integração avançada de dados governamentais em larga escala.

Este módulo fornece funcionalidades para processamento de dados reais grandes,
incluindo arquivos SIAFI com dezenas de milhares de registros.

Classes:
    AdvancedDataIntegrator: Integrador para processamento de dados em larga escala
"""

import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)


class AdvancedDataIntegrator:
    """
    Integrador avançado para processar dados governamentais em larga escala.
    
    Specialized for handling real government data including large SIAFI files
    with 48k+ records.
    """
    
    def __init__(self, raw_data_dir: str = "data/raw", processed_data_dir: str = "data/processed"):
        """
        Inicializa o integrador avançado.

        Args:
            raw_data_dir: Diretório com dados brutos
            processed_data_dir: Diretório para dados processados
        """
        self.raw_dir = Path(raw_data_dir)
        self.processed_dir = Path(processed_data_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Mapeamento para identificar colunas-chave por fonte
        self.key_mappings = {
            "siafi": [
                "Código Órgão Superior",
                "Código Unidade Gestora", 
                "Valor Empenhado (R$)",
            ],
            "compras": ["uasg", "valor_total", "cnpj_contratada"],
            "transferegov": ["codigo_siafi", "valor_liberado", "beneficiario"],
        }
        
        logger.info("AdvancedDataIntegrator inicializado")
        logger.info(f"Diretório de dados brutos: {self.raw_dir}")
        logger.info(f"Diretório de dados processados: {self.processed_dir}")

    def detect_file_source(self, filename: str) -> str:
        """
        Detecta a fonte do arquivo baseado no nome.
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            Fonte detectada (siafi, compras, transferegov, unknown)
        """
        filename_lower = filename.lower()

        if any(x in filename_lower for x in ["siafi", "despesas", "orcament"]):
            return "siafi"
        elif any(x in filename_lower for x in ["contrato", "compras", "licitac"]):
            return "compras"
        elif any(x in filename_lower for x in ["convenio", "transfere", "transfer"]):
            return "transferegov"
        else:
            return "unknown"

    def load_large_csv_safely(self, filepath: Path, max_rows: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Carrega arquivo CSV grande de forma segura com múltiplos encodings.
        
        Args:
            filepath: Caminho para o arquivo
            max_rows: Número máximo de registros a carregar
            
        Returns:
            DataFrame carregado ou None se falhar
        """
        try:
            logger.info(f"Carregando arquivo: {filepath.name}")

            # Tentar diferentes encodings
            encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
            separators = [";", ","]
            
            df = None

            for encoding in encodings:
                for sep in separators:
                    try:
                        kwargs = {
                            "encoding": encoding,
                            "sep": sep,
                            "on_bad_lines": "skip"  # Pular linhas problemáticas
                        }
                        
                        if max_rows:
                            kwargs["nrows"] = max_rows
                        
                        df = pd.read_csv(filepath, **kwargs)
                        logger.info(f"Arquivo carregado com encoding: {encoding}, separador: '{sep}'")
                        break
                        
                    except (UnicodeDecodeError, pd.errors.ParserError):
                        continue
                    except Exception as e:
                        logger.debug(f"Erro com encoding {encoding}, sep '{sep}': {e}")
                        continue
                
                if df is not None:
                    break

            if df is None:
                logger.error(f"Não foi possível carregar {filepath}")
                return None

            logger.info(f"✅ Carregados {len(df)} registros de {filepath.name}")
            logger.info(f"   📊 Colunas: {list(df.columns)[:5]}...")
            
            return df

        except Exception as e:
            logger.error(f"❌ Erro ao carregar {filepath}: {e}")
            return None

    def process_siafi_data_advanced(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Processa dados do SIAFI para formato padronizado avançado.
        
        Args:
            df: DataFrame com dados SIAFI brutos
            
        Returns:
            DataFrame processado ou None se falhar
        """
        try:
            logger.info("🏛️ Processando dados SIAFI...")
            
            # Identificar colunas importantes do SIAFI
            value_col = None
            org_col = None
            unit_col = None

            # Procurar colunas por palavras-chave
            for col in df.columns:
                col_lower = col.lower()
                if "valor" in col_lower and "empenhado" in col_lower:
                    value_col = col
                elif "órgão superior" in col_lower or "orgao superior" in col_lower:
                    org_col = col
                elif "unidade gestora" in col_lower:
                    unit_col = col

            if not value_col:
                logger.warning("Coluna de valor não encontrada no SIAFI")
                # Tentar encontrar qualquer coluna com 'valor'
                value_cols = [col for col in df.columns if "valor" in col.lower()]
                if value_cols:
                    value_col = value_cols[0]
                    logger.info(f"Usando coluna de valor alternativa: {value_col}")

            # Criar DataFrame processado
            processed = pd.DataFrame()

            if org_col:
                processed["orgao_superior"] = df[org_col]
            if unit_col:
                processed["unidade_gestora"] = df[unit_col]
            if value_col:
                # Limpar valores monetários
                processed["valor_empenhado"] = self._clean_monetary_values(df[value_col])

            # Adicionar outras colunas relevantes (se existirem)
            for col in df.columns:
                col_lower = col.lower()
                if "data" in col_lower:
                    processed[f"data_{col.lower().replace(' ', '_')}"] = df[col]
                elif "codigo" in col_lower or "código" in col_lower:
                    processed[f"codigo_{col.lower().replace(' ', '_')}"] = df[col]

            # Adicionar metadados
            processed["fonte"] = "SIAFI"
            processed["data_processamento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.info(f"✅ SIAFI processado: {len(processed)} registros")
            
            # Estatísticas básicas
            if "valor_empenhado" in processed.columns:
                total_value = processed["valor_empenhado"].sum()
                logger.info(f"💰 Valor total empenhado: R$ {total_value:,.2f}")
            
            return processed

        except Exception as e:
            logger.error(f"❌ Erro ao processar SIAFI: {e}")
            return None

    def _clean_monetary_values(self, series: pd.Series) -> pd.Series:
        """
        Limpa valores monetários para formato numérico.
        
        Args:
            series: Série com valores monetários
            
        Returns:
            Série com valores numéricos limpos
        """
        try:
            # Converter para string e limpar
            cleaned = (
                series.astype(str)
                .str.replace(",", ".")
                .str.replace('"', "")
                .str.replace("R$", "")
                .str.replace(" ", "")
                .str.strip()
            )
            
            # Converter para numérico
            return pd.to_numeric(cleaned, errors="coerce")
            
        except Exception as e:
            logger.warning(f"Erro ao limpar valores monetários: {e}")
            return series

    def process_all_available_files(self, max_large_file_rows: int = 1000) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Dict]]:
        """
        Processa todos os arquivos disponíveis no diretório.
        
        Args:
            max_large_file_rows: Número máximo de registros para arquivos grandes
            
        Returns:
            Tupla com dados processados e estatísticas
        """
        logger.info("🔄 === Iniciando processamento completo de arquivos ===")

        all_data = {}
        summary_stats = {}

        # Listar todos os arquivos CSV
        csv_files = list(self.raw_dir.glob("*.csv"))
        logger.info(f"📁 Encontrados {len(csv_files)} arquivos CSV")

        for file_path in csv_files:
            logger.info(f"\n--- Processando: {file_path.name} ---")

            source = self.detect_file_source(file_path.name)
            logger.info(f"🏷️ Fonte detectada: {source}")

            # Verificar tamanho do arquivo
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            logger.info(f"📏 Tamanho: {file_size_mb:.1f} MB")

            # Determinar estratégia de carregamento
            max_rows = None
            if file_size_mb > 10:  # Arquivos maiores que 10MB
                max_rows = max_large_file_rows
                logger.info(f"📊 Arquivo grande detectado, limitando a {max_rows} registros")

            # Carregar arquivo
            df = self.load_large_csv_safely(file_path, max_rows=max_rows)

            if df is not None and len(df) > 0:
                # Processar baseado na fonte detectada
                processed_df = df
                
                if source == "siafi" and file_size_mb > 1:  # SIAFI real
                    processed_df = self.process_siafi_data_advanced(df)
                    if processed_df is not None:
                        all_data[f"siafi_real_{file_path.stem}"] = processed_df
                        summary_stats[file_path.name] = {
                            "fonte": "SIAFI (Real)",
                            "registros": len(processed_df),
                            "tamanho_mb": file_size_mb,
                            "valor_total": (
                                processed_df["valor_empenhado"].sum()
                                if "valor_empenhado" in processed_df.columns
                                else 0
                            ),
                        }
                else:
                    # Outros arquivos (samples ou pequenos)
                    all_data[f"{source}_{file_path.stem}"] = processed_df
                    summary_stats[file_path.name] = {
                        "fonte": source.upper(),
                        "registros": len(processed_df),
                        "tamanho_mb": file_size_mb,
                        "principais_colunas": list(processed_df.columns)[:3],
                    }

        return all_data, summary_stats

    def generate_comprehensive_report(self, all_data: Dict[str, pd.DataFrame], summary_stats: Dict[str, Dict]) -> str:
        """
        Gera relatório abrangente dos dados processados.
        
        Args:
            all_data: Dados processados
            summary_stats: Estatísticas dos arquivos
            
        Returns:
            Relatório em formato texto
        """
        report_lines = [
            "=== RELATÓRIO AVANÇADO DE INTEGRAÇÃO - GOV-HUB ===",
            f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        # Estatísticas gerais
        total_files = len(summary_stats)
        total_records = sum(stats["registros"] for stats in summary_stats.values())
        total_size_mb = sum(stats["tamanho_mb"] for stats in summary_stats.values())

        report_lines.extend([
            "📊 ESTATÍSTICAS GERAIS:",
            f"   • Total de arquivos processados: {total_files}",
            f"   • Total de registros: {total_records:,}",
            f"   • Volume total de dados: {total_size_mb:.1f} MB",
            "",
        ])

        # Análise detalhada por arquivo
        report_lines.append("📁 ANÁLISE DETALHADA:")
        for filename, stats in summary_stats.items():
            report_lines.append(f"   📄 {filename}")
            report_lines.append(f"      Fonte: {stats['fonte']}")
            report_lines.append(f"      Registros: {stats['registros']:,}")
            report_lines.append(f"      Tamanho: {stats['tamanho_mb']:.1f} MB")

            if "valor_total" in stats and stats["valor_total"] > 0:
                report_lines.append(f"      Valor Total: R$ {stats['valor_total']:,.2f}")

            if "principais_colunas" in stats:
                report_lines.append(f"      Principais colunas: {', '.join(stats['principais_colunas'])}")
            
            report_lines.append("")

        # Consolidação por fonte
        sources_summary = {}
        for stats in summary_stats.values():
            fonte = stats["fonte"]
            if fonte not in sources_summary:
                sources_summary[fonte] = {"arquivos": 0, "registros": 0, "tamanho_mb": 0}
            sources_summary[fonte]["arquivos"] += 1
            sources_summary[fonte]["registros"] += stats["registros"]
            sources_summary[fonte]["tamanho_mb"] += stats["tamanho_mb"]

        report_lines.extend(["🎯 CONSOLIDAÇÃO POR FONTE:", ""])
        for fonte, dados in sources_summary.items():
            report_lines.extend([
                f"   🏷️ {fonte}:",
                f"      Arquivos: {dados['arquivos']}",
                f"      Registros: {dados['registros']:,}",
                f"      Volume: {dados['tamanho_mb']:.1f} MB",
                "",
            ])

        # Avaliação da qualidade dos dados
        real_sources = [s for s in sources_summary.keys() if "Real" in s]
        report_lines.extend([
            "⭐ AVALIAÇÃO DA QUALIDADE:",
            f"   • Fontes com dados reais: {len(real_sources)}",
            f"   • Maior arquivo processado: {max(stats['tamanho_mb'] for stats in summary_stats.values()):.1f} MB",
            f"   • Cobertura estimada: {len(real_sources)/3*100:.1f}%",
            "",
        ])

        return "\n".join(report_lines)

    def save_integration_results(self, all_data: Dict[str, pd.DataFrame], summary_stats: Dict[str, Dict]) -> Tuple[Path, Path]:
        """
        Salva resultados da integração avançada.
        
        Args:
            all_data: Dados processados
            summary_stats: Estatísticas dos arquivos
            
        Returns:
            Caminhos do relatório e resumo executivo
        """
        # Gerar e salvar relatório completo
        report_content = self.generate_comprehensive_report(all_data, summary_stats)
        report_path = self.processed_dir / "advanced_integration_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        logger.info(f"✅ Relatório avançado salvo: {report_path}")

        # Salvar dados SIAFI processados (se disponível)
        siafi_data = None
        for key, df in all_data.items():
            if "siafi_real" in key and isinstance(df, pd.DataFrame):
                siafi_data = df
                break

        if siafi_data is not None:
            siafi_path = self.processed_dir / "siafi_advanced_processed.csv"
            siafi_data.to_csv(siafi_path, index=False, encoding="utf-8")
            logger.info(f"✅ Dados SIAFI avançados salvos: {siafi_path}")

        # Criar resumo executivo
        executive_summary = [
            "=== RESUMO EXECUTIVO - INTEGRAÇÃO AVANÇADA ===",
            f"Execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "📊 RESULTADOS:",
            f"   • {len(all_data)} conjuntos de dados processados",
            f"   • {sum(len(df) if isinstance(df, pd.DataFrame) else 0 for df in all_data.values()):,} registros totais",
            "   • Processamento avançado de dados reais implementado",
            "",
            "🎯 CONQUISTAS:",
            "   ✅ Sistema robusto de carregamento de arquivos grandes",
            "   ✅ Processamento inteligente de dados SIAFI",
            "   ✅ Relatórios abrangentes e estatísticas detalhadas",
            "   ✅ Tratamento de múltiplos encodings e separadores",
            "",
            "🚀 PRÓXIMOS PASSOS:",
            "   1. Implementar dashboards interativos",
            "   2. Otimizar APIs de Compras e TransfereGov",
            "   3. Agendar execução automática",
            "   4. Adicionar análises preditivas",
        ]

        summary_path = self.processed_dir / "executive_summary_advanced.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("\n".join(executive_summary))
        logger.info(f"✅ Resumo executivo salvo: {summary_path}")

        return report_path, summary_path

    def execute_advanced_integration(self) -> bool:
        """
        Executa o pipeline completo de integração avançada.
        
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            logger.info("🚀 === Iniciando Integração Avançada ===")

            # Processar todos os arquivos
            all_data, summary_stats = self.process_all_available_files(max_large_file_rows=1000)

            if not all_data:
                logger.warning("⚠️ Nenhum dado foi processado")
                return False

            # Salvar resultados
            report_path, summary_path = self.save_integration_results(all_data, summary_stats)

            logger.info("\n" + "=" * 60)
            logger.info("🎉 === INTEGRAÇÃO AVANÇADA CONCLUÍDA ===")
            logger.info(f"📄 Relatório detalhado: {report_path}")
            logger.info(f"📄 Resumo executivo: {summary_path}")

            return True

        except Exception as e:
            logger.error(f"❌ Erro crítico na integração avançada: {e}")
            return False


def main():
    """Função principal para execução standalone."""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
    )
    
    try:
        integrator = AdvancedDataIntegrator()
        success = integrator.execute_advanced_integration()
        return 0 if success else 1
        
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
