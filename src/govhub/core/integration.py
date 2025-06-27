#!/usr/bin/env python3
"""
Gov-Hub Data Integration Module
Módulo para integração e processamento de dados governamentais.

Este módulo fornece a classe DataIntegrator para processamento
e integração de dados do SIAFI, Compras.gov.br e TransfereGov.

Classes:
    DataIntegrator: Classe principal para integração de dados
"""

import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class DataIntegrator:
    """
    Classe principal para integração de dados governamentais.
    
    Esta classe implementa funcionalidades para:
    - Carregamento de dados CSV
    - Integração entre diferentes fontes
    - Geração de relatórios de correspondência
    - Salvamento de dados processados
    """

    def __init__(self, raw_data_dir: str = "data/raw", processed_data_dir: str = "data/processed"):
        """
        Inicializa o Data Integrator.

        Args:
            raw_data_dir: Diretório com dados brutos
            processed_data_dir: Diretório para dados processados
        """
        self.raw_dir = Path(raw_data_dir)
        self.processed_dir = Path(processed_data_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("DataIntegrator inicializado")
        logger.info(f"Diretório de dados brutos: {self.raw_dir}")
        logger.info(f"Diretório de dados processados: {self.processed_dir}")

    def load_csv_file_data(self, filename: str) -> List[Dict]:
        """
        Carrega dados de um arquivo CSV.

        Args:
            filename: Nome do arquivo CSV

        Returns:
            Lista de dicionários com os dados
        """
        filepath = self.raw_dir / filename

        if not filepath.exists():
            logger.warning(f"Arquivo {filename} não encontrado")
            return []

        data = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            logger.info(f"Carregados {len(data)} registros de {filename}")
        except Exception as e:
            logger.error(f"Erro ao carregar {filename}: {e}")

        return data

    def discover_latest_files(self) -> Dict[str, Optional[str]]:
        """
        Encontra os arquivos mais recentes de cada fonte.

        Returns:
            Dicionário com nomes dos arquivos mais recentes
        """
        files = {"siafi": None, "compras": None, "transferegov": None}

        # Procurar arquivos mais recentes por padrão de nome
        for file_path in self.raw_dir.glob("*.csv"):
            filename = file_path.name.lower()
            if "siafi" in filename:
                if not files["siafi"] or filename > files["siafi"].lower():
                    files["siafi"] = file_path.name
            elif "contrato" in filename or "compras" in filename:
                if not files["compras"] or filename > files["compras"].lower():
                    files["compras"] = file_path.name
            elif "convenio" in filename or "transfere" in filename:
                if not files["transferegov"] or filename > files["transferegov"].lower():
                    files["transferegov"] = file_path.name

        logger.info("Arquivos descobertos:")
        for source, filename in files.items():
            if filename:
                logger.info(f"  {source.upper()}: {filename}")
            else:
                logger.warning(f"  {source.upper()}: Nenhum arquivo encontrado")

        return files

    def integrate_government_data(self) -> Tuple[List[Dict], Dict[str, int], Dict[str, int]]:
        """
        Integra dados de diferentes fontes governamentais.

        Returns:
            Tupla com (dados_integrados, estatísticas_matches, contadores)
        """
        files = self.discover_latest_files()

        # Carregar dados de cada fonte
        siafi_data = self.load_csv_file_data(files["siafi"]) if files["siafi"] else []
        compras_data = self.load_csv_file_data(files["compras"]) if files["compras"] else []
        transfere_data = (
            self.load_csv_file_data(files["transferegov"]) if files["transferegov"] else []
        )

        # Criar índices para join eficiente
        compras_index = self._create_compras_index(compras_data)
        transfere_index = self._create_transferegov_index(transfere_data)

        # Integrar dados usando código UG como chave
        integrated_data = []
        matches = {"siafi_compras": 0, "siafi_transfere": 0, "total_integrated": 0}

        for siafi_row in siafi_data:
            codigo_ug = siafi_row.get("codigo_ug", "")

            # Criar linha integrada começando com dados do SIAFI
            integrated_row = dict(siafi_row)

            # Join com dados de compras
            if codigo_ug in compras_index:
                compras_row = compras_index[codigo_ug]
                for key, value in compras_row.items():
                    integrated_row[f"compras_{key}"] = value
                matches["siafi_compras"] += 1

            # Join com dados do TransfereGov
            if codigo_ug in transfere_index:
                transfere_row = transfere_index[codigo_ug]
                for key, value in transfere_row.items():
                    integrated_row[f"transfere_{key}"] = value
                matches["siafi_transfere"] += 1

            integrated_data.append(integrated_row)
            matches["total_integrated"] += 1

        logger.info(f"Integração concluída: {matches['total_integrated']} registros processados")
        logger.info(f"Matches SIAFI-Compras: {matches['siafi_compras']}")
        logger.info(f"Matches SIAFI-TransfereGov: {matches['siafi_transfere']}")

        return (
            integrated_data,
            matches,
            {
                "siafi": len(siafi_data),
                "compras": len(compras_data),
                "transferegov": len(transfere_data),
            },
        )

    def _create_compras_index(self, compras_data: List[Dict]) -> Dict[str, Dict]:
        """
        Cria índice de dados de compras por UASG.

        Args:
            compras_data: Lista com dados de compras

        Returns:
            Dicionário indexado por UASG
        """
        index = {}
        for row in compras_data:
            uasg = row.get("uasg", "")
            if uasg:
                index[uasg] = row
        
        logger.info(f"Índice de compras criado: {len(index)} entradas")
        return index

    def _create_transferegov_index(self, transfere_data: List[Dict]) -> Dict[str, Dict]:
        """
        Cria índice de dados do TransfereGov por código SIAFI.

        Args:
            transfere_data: Lista com dados do TransfereGov

        Returns:
            Dicionário indexado por código SIAFI
        """
        index = {}
        for row in transfere_data:
            codigo_siafi = row.get("codigo_siafi", "")
            if codigo_siafi:
                index[codigo_siafi] = row
        
        logger.info(f"Índice do TransfereGov criado: {len(index)} entradas")
        return index

    def save_integrated_data_to_csv(self, integrated_data: List[Dict]) -> bool:
        """
        Salva os dados integrados em arquivo CSV.

        Args:
            integrated_data: Lista com dados integrados

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if not integrated_data:
            logger.warning("Nenhum dado para salvar")
            return False

        output_file = self.processed_dir / "integrated_poc_data.csv"

        try:
            # Obter todas as colunas únicas
            all_columns = set()
            for row in integrated_data:
                all_columns.update(row.keys())
            all_columns = sorted(list(all_columns))

            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=all_columns)
                writer.writeheader()
                writer.writerows(integrated_data)

            file_size = output_file.stat().st_size / 1024  # KB
            logger.info(f"Dados integrados salvos em {output_file}")
            logger.info(f"Arquivo gerado: {len(integrated_data)} registros, {file_size:.1f} KB")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar dados integrados: {e}")
            return False

    def generate_integration_summary(self, matches: Dict[str, int], counts: Dict[str, int]) -> bool:
        """
        Gera relatório de resumo da integração.

        Args:
            matches: Estatísticas de correspondências
            counts: Contadores por fonte

        Returns:
            True se gerou com sucesso, False caso contrário
        """
        # Calcular taxas de correspondência
        siafi_count = max(counts["siafi"], 1)  # Evitar divisão por zero
        compras_rate = (matches["siafi_compras"] / siafi_count) * 100
        transfere_rate = (matches["siafi_transfere"] / siafi_count) * 100

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
            f"- SIAFI-Compras: {compras_rate:.1f}%",
            f"- SIAFI-TransfereGov: {transfere_rate:.1f}%",
            "",
            "Status: INTEGRACAO CONCLUIDA COM SUCESSO!",
            "",
            "Arquivos Gerados:",
            "- data/processed/integrated_poc_data.csv (dados integrados)",
            "- data/processed/poc_summary.txt (este relatorio)",
        ]

        summary_file = self.processed_dir / "poc_summary.txt"
        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write("\n".join(summary_lines))
            
            file_size = summary_file.stat().st_size
            logger.info(f"Relatório salvo em {summary_file}")
            logger.info(f"Relatório gerado: {len(summary_lines)} linhas, {file_size} bytes")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {e}")
            return False

    def execute_complete_integration(self) -> bool:
        """
        Executa o processo completo de integração.

        Returns:
            True se concluiu com sucesso, False caso contrário
        """
        try:
            logger.info("=== Iniciando integração de dados governamentais ===")

            # Integrar dados
            integrated_data, matches, counts = self.integrate_government_data()

            if not integrated_data:
                logger.error("Nenhum dado foi integrado")
                return False

            # Salvar dados integrados
            if not self.save_integrated_data_to_csv(integrated_data):
                logger.error("Falha ao salvar dados integrados")
                return False

            # Gerar relatório de resumo
            if not self.generate_integration_summary(matches, counts):
                logger.warning("Falha ao gerar relatório de resumo")

            logger.info("=== Integração concluída com sucesso ===")
            return True

        except Exception as e:
            logger.error(f"Erro durante a integração: {e}")
            return False


def main():
    """Função principal para execução standalone."""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    integrator = DataIntegrator()
    success = integrator.execute_complete_integration()
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
