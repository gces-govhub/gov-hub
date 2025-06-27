#!/usr/bin/env python3
"""
Gov-Hub Data Acquisition Module
Sistema robusto de aquisição de dados governamentais brasileiros.

Este módulo fornece a classe GovHubDataAcquirer para download e processamento
de dados de fontes como SIAFI, Compras.gov.br e TransfereGov.

Classes:
    GovHubDataAcquirer: Classe principal para aquisição de dados
"""

import argparse
import json
import logging
import ssl
import time
import zipfile
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

# Configuração de SSL para evitar erros de certificado
ssl._create_default_https_context = ssl._create_unverified_context

# Configuração de logging
logger = logging.getLogger(__name__)


class GovHubDataAcquirer:
    """
    Classe principal para aquisição robusta de dados governamentais.
    
    Esta classe implementa funcionalidades para:
    - Download de dados do SIAFI
    - Download de dados do Compras.gov.br
    - Download de dados do TransfereGov
    - Fallback automático para dados de amostra
    - Tratamento robusto de exceções
    """

    def __init__(self, config_path: str = "config/config.json"):
        """
        Inicializa o Data Acquirer com configurações externas.

        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        self.config = self._load_configuration(config_path)
        self.output_dir = Path(self.config["file_settings"]["raw_data_dir"])
        self.temp_dir = Path(self.config["file_settings"]["temp_dir"])

        # Criar diretórios necessários
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        # Configurações de download
        self.timeout = self.config["download_settings"]["timeout"]
        self.chunk_size = self.config["download_settings"]["chunk_size"]
        self.max_retries = self.config["download_settings"]["max_retries"]
        self.retry_delay = self.config["download_settings"]["retry_delay"]
        self.rate_limit_delay = self.config["download_settings"]["rate_limit_delay"]

        logger.info("GovHub Data Acquirer inicializado com sucesso")
        logger.info(f"Diretório de saída: {self.output_dir}")
        logger.info(f"Diretório temporário: {self.temp_dir}")

    def _load_configuration(self, config_path: str) -> Dict:
        """Carrega configurações do arquivo JSON."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.info(f"Configurações carregadas de: {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Arquivo de configuração não encontrado: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            raise

    def _make_http_request(
        self,
        url: str,
        headers: Dict,
        params: Optional[Dict] = None,
        stream: bool = False,
    ) -> Optional[requests.Response]:
        """
        Realiza requisição HTTP com tratamento robusto de erros.

        Args:
            url: URL para requisição
            headers: Headers HTTP
            params: Parâmetros da URL
            stream: Se deve fazer download em stream

        Returns:
            Response object ou None se falhou
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    f"Tentativa {attempt}/{self.max_retries} - Acessando: {url}"
                )

                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout,
                    stream=stream,
                    verify=False,  # Para evitar problemas com SSL em alguns portais gov
                )

                # Log do status da resposta
                logger.info(f"Status HTTP: {response.status_code}")
                if (
                    hasattr(response, "headers")
                    and "content-length" in response.headers
                ):
                    size_mb = int(response.headers["content-length"]) / (1024 * 1024)
                    logger.info(f"Tamanho do arquivo: {size_mb:.2f} MB")

                # Verificar códigos de erro específicos
                if response.status_code == 403:
                    logger.warning(f"Acesso negado (403) para: {url}")
                    logger.warning(
                        "Possível bloqueio por User-Agent ou necessidade de autenticação"
                    )
                    return None
                elif response.status_code == 404:
                    logger.warning(f"Recurso não encontrado (404): {url}")
                    return None
                elif response.status_code == 429:
                    logger.warning(
                        f"Rate limit atingido (429). Aguardando {self.retry_delay * 2}s..."
                    )
                    time.sleep(self.retry_delay * 2)
                    continue

                # Se chegou aqui, verificar se é sucesso
                response.raise_for_status()

                logger.info("✅ Requisição realizada com sucesso")
                return response

            except requests.exceptions.Timeout:
                logger.warning(
                    f"Timeout na tentativa {attempt}. Aguardando {self.retry_delay}s..."
                )
                time.sleep(self.retry_delay)

            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Erro de conexão na tentativa {attempt}: {e}")
                time.sleep(self.retry_delay)

            except requests.exceptions.RequestException as e:
                logger.error(f"Erro na requisição (tentativa {attempt}): {e}")
                if attempt == self.max_retries:
                    return None
                time.sleep(self.retry_delay)

        logger.error(f"❌ Falha após {self.max_retries} tentativas para: {url}")
        return None

    def _extract_zip_content(self, zip_path: Path, extract_to: Path) -> bool:
        """
        Extrai arquivo ZIP e processa arquivos CSV.

        Args:
            zip_path: Caminho para o arquivo ZIP
            extract_to: Diretório de destino

        Returns:
            True se extraiu com sucesso, False caso contrário
        """
        try:
            logger.info(f"Extraindo arquivo ZIP: {zip_path}")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Listar conteúdo do ZIP
                file_list = zip_ref.namelist()
                logger.info(f"Arquivos no ZIP: {file_list}")

                # Extrair todos os arquivos
                zip_ref.extractall(extract_to)

                # Procurar por arquivos CSV e mover para o diretório principal
                csv_files = [f for f in file_list if f.lower().endswith(".csv")]

                for csv_file in csv_files:
                    src_path = extract_to / csv_file
                    if src_path.exists():
                        # Criar nome de arquivo único com timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d")
                        new_name = f"{Path(csv_file).stem}_{timestamp}.csv"
                        dest_path = self.output_dir / new_name

                        # Mover arquivo
                        src_path.rename(dest_path)
                        logger.info(f"✅ Arquivo CSV extraído: {dest_path}")

                # Remover arquivo ZIP temporário
                zip_path.unlink()

                return len(csv_files) > 0

        except zipfile.BadZipFile:
            logger.error(f"❌ Arquivo ZIP corrompido: {zip_path}")
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao extrair ZIP: {e}")
            return False

    def _download_large_file(self, url: str, headers: Dict, filename: str) -> Optional[Path]:
        """
        Baixa arquivo grande usando streaming.

        Args:
            url: URL do arquivo
            headers: Headers HTTP
            filename: Nome do arquivo de destino

        Returns:
            Caminho para o arquivo baixado ou None se falhou
        """
        response = self._make_http_request(url, headers, stream=True)
        if not response:
            return None

        try:
            # Determinar se é ZIP ou CSV pelo Content-Type ou URL
            content_type = response.headers.get("content-type", "").lower()
            if "zip" in content_type or url.lower().endswith(".zip"):
                file_path = self.temp_dir / f"{filename}.zip"
            else:
                file_path = self.output_dir / f"{filename}.csv"

            # Download com progress
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            logger.info(f"Iniciando download para: {file_path}")

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Log de progresso a cada 10MB
                        if downloaded % (10 * 1024 * 1024) == 0:
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                logger.info(
                                    f"Download: {progress:.1f}% ({downloaded / (1024*1024):.1f}MB)"
                                )

            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Download concluído: {file_path} ({file_size_mb:.2f}MB)")

            # Se for ZIP, extrair
            if str(file_path).endswith(".zip"):
                if self._extract_zip_content(file_path, self.temp_dir):
                    logger.info("✅ Arquivo ZIP extraído com sucesso")
                else:
                    logger.warning("⚠️ Problemas na extração do ZIP")

            return file_path

        except Exception as e:
            logger.error(f"❌ Erro durante o download: {e}")
            return None

    def download_siafi_data(self) -> bool:
        """
        Baixa dados do SIAFI de múltiplas fontes.

        Returns:
            True se pelo menos uma fonte teve sucesso, False caso contrário
        """
        logger.info("🏛️ === Iniciando download dos dados do SIAFI ===")

        siafi_config = self.config["data_sources"]["siafi"]
        logger.info(f"Fonte: {siafi_config['name']}")

        success = False

        for i, url_config in enumerate(siafi_config["urls"], 1):
            logger.info(f"\n--- Tentativa {i}: {url_config['description']} ---")

            try:
                url = url_config["url"]
                headers = url_config["headers"]

                # Para URLs que precisam de parâmetros específicos
                if "despesas-execucao" in url and not url.endswith(("csv", "zip")):
                    current_year = datetime.now().year
                    url = f"{url}/{current_year}01"

                logger.info(f"URL final: {url}")

                timestamp = datetime.now().strftime("%Y-%m-%d")
                filename = f"siafi_{timestamp}"

                downloaded_file = self._download_large_file(url, headers, filename)

                if downloaded_file:
                    logger.info(f"✅ Download do SIAFI bem-sucedido: {downloaded_file}")
                    success = True
                    break

            except Exception as e:
                logger.error(f"❌ Erro inesperado na fonte {i}: {e}")
                continue

            time.sleep(self.rate_limit_delay)

        if not success:
            logger.warning(
                "⚠️ Todas as fontes SIAFI falharam. Gerando dados de amostra..."
            )
            self._generate_sample_data("siafi")

        return success

    def download_compras_data(self) -> bool:
        """
        Baixa dados do Compras.gov.br.

        Returns:
            True se pelo menos uma fonte teve sucesso
        """
        logger.info("🛒 === Iniciando download dos dados do Compras.gov.br ===")

        compras_config = self.config["data_sources"]["compras"]
        success = False

        for i, url_config in enumerate(compras_config["urls"], 1):
            try:
                url = url_config["url"]
                headers = url_config["headers"]

                if url_config["format"] == "json":
                    success_paginated = self._download_paginated_json_data(
                        url, headers, "compras"
                    )
                    if success_paginated:
                        success = True
                        break
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d")
                    filename = f"contratos_{timestamp}"

                    downloaded_file = self._download_large_file(url, headers, filename)

                    if downloaded_file:
                        logger.info(
                            f"✅ Download de Compras bem-sucedido: {downloaded_file}"
                        )
                        success = True
                        break

            except Exception as e:
                logger.error(f"❌ Erro inesperado na fonte {i}: {e}")
                continue

            time.sleep(self.rate_limit_delay)

        if not success:
            logger.warning(
                "⚠️ Todas as fontes de Compras falharam. Gerando dados de amostra..."
            )
            self._generate_sample_data("compras")

        return success

    def download_transferegov_data(self) -> bool:
        """
        Baixa dados do TransfereGov.

        Returns:
            True se pelo menos uma fonte teve sucesso
        """
        logger.info("💰 === Iniciando download dos dados do TransfereGov ===")

        transfere_config = self.config["data_sources"]["transferegov"]
        success = False

        for i, url_config in enumerate(transfere_config["urls"], 1):
            try:
                url = url_config["url"]
                headers = url_config["headers"]

                if url_config["format"] == "json":
                    success_api = self._download_transferegov_api_data(url, headers)
                    if success_api:
                        success = True
                        break
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d")
                    filename = f"convenios_{timestamp}"

                    downloaded_file = self._download_large_file(url, headers, filename)

                    if downloaded_file:
                        logger.info(
                            f"✅ Download de TransfereGov bem-sucedido: {downloaded_file}"
                        )
                        success = True
                        break

            except Exception as e:
                logger.error(f"❌ Erro inesperado na fonte {i}: {e}")
                continue

            time.sleep(self.rate_limit_delay)

        if not success:
            logger.warning(
                "⚠️ Todas as fontes de TransfereGov falharam. Gerando dados de amostra..."
            )
            self._generate_sample_data("transferegov")

        return success

    def _download_paginated_json_data(
        self, base_url: str, headers: Dict, resource_name: str
    ) -> bool:
        """
        Baixa dados JSON com paginação automática.

        Args:
            base_url: URL base da API
            headers: Headers HTTP
            resource_name: Nome do recurso

        Returns:
            True se teve sucesso
        """
        try:
            all_data = []
            page = 0
            max_pages = self.config["download_settings"]["max_pages"]

            while page < max_pages:
                params = {"offset": page * 100, "limit": 100}

                logger.info(f"Baixando página {page + 1}/{max_pages}...")

                response = self._make_http_request(base_url, headers, params)
                if not response:
                    break

                try:
                    data = response.json()

                    if isinstance(data, list):
                        page_data = data
                    elif isinstance(data, dict):
                        page_data = data.get(
                            "data", data.get("results", data.get("items", []))
                        )
                    else:
                        logger.warning(f"Estrutura de resposta inesperada: {type(data)}")
                        break

                    if not page_data:
                        logger.info("Não há mais dados para baixar")
                        break

                    all_data.extend(page_data)
                    logger.info(f"Página {page + 1}: {len(page_data)} registros coletados")

                    if len(page_data) < 100:
                        logger.info("Última página atingida")
                        break

                    page += 1
                    time.sleep(self.rate_limit_delay)

                except json.JSONDecodeError:
                    logger.error("Erro ao decodificar resposta JSON")
                    break

            if all_data:
                df = pd.DataFrame(all_data)
                timestamp = datetime.now().strftime("%Y-%m-%d")
                output_file = self.output_dir / f"{resource_name}_{timestamp}.csv"

                df.to_csv(output_file, index=False, encoding="utf-8")
                logger.info(f"✅ {len(all_data)} registros salvos em: {output_file}")
                return True
            else:
                logger.warning("Nenhum dado foi coletado")
                return False

        except Exception as e:
            logger.error(f"❌ Erro na coleta paginada: {e}")
            return False

    def _download_transferegov_api_data(self, url: str, headers: Dict) -> bool:
        """
        Método específico para API do TransfereGov.

        Args:
            url: URL da API
            headers: Headers HTTP

        Returns:
            True se teve sucesso
        """
        try:
            logger.info("Acessando API específica do TransfereGov...")

            response = self._make_http_request(url, headers)
            if not response:
                return False

            try:
                data = response.json()

                if isinstance(data, list):
                    records = data
                elif isinstance(data, dict):
                    records = data.get(
                        "data", data.get("transferencias", data.get("convenios", []))
                    )
                else:
                    logger.warning(f"Estrutura inesperada da API TransfereGov: {type(data)}")
                    return False

                if records:
                    df = pd.DataFrame(records)
                    timestamp = datetime.now().strftime("%Y-%m-%d")
                    output_file = self.output_dir / f"transferegov_{timestamp}.csv"

                    df.to_csv(output_file, index=False, encoding="utf-8")
                    logger.info(
                        f"✅ {len(records)} registros TransfereGov salvos em: {output_file}"
                    )
                    return True
                else:
                    logger.warning("API TransfereGov retornou dados vazios")
                    return False

            except json.JSONDecodeError:
                logger.error("Erro ao decodificar resposta JSON do TransfereGov")
                return False

        except Exception as e:
            logger.error(f"❌ Erro específico TransfereGov: {e}")
            return False

    def _generate_sample_data(self, resource: str) -> None:
        """
        Gera dados de amostra quando falha o download real.

        Args:
            resource: Nome do recurso (siafi, compras, transferegov)
        """
        logger.warning(f"🔄 Gerando dados de amostra para {resource.upper()}...")

        timestamp = datetime.now().strftime("%Y-%m-%d")

        if resource == "siafi":
            data = {
                "codigo_ug": ["153978", "153979", "154357", "154358", "154359"],
                "orgao": ["26291", "26291", "26291", "36000", "36000"],
                "gestao": ["15256", "15256", "15256", "15256", "15256"],
                "numero_empenho": [
                    "2025NE000123",
                    "2025NE000124",
                    "2025NE000125",
                    "2025NE000126",
                    "2025NE000127",
                ],
                "valor_empenhado": [150000.00, 75000.50, 200000.00, 95000.75, 180000.25],
                "credor": [
                    "12345678000123",
                    "98765432000876",
                    "45678901000567",
                    "32109876000210",
                    "78901234000890",
                ],
                "data_empenho": [
                    "2025-01-15",
                    "2025-02-20",
                    "2025-03-10",
                    "2025-04-05",
                    "2025-05-12",
                ],
                "funcao": ["Administração", "Educação", "Saúde", "Segurança", "Transporte"],
            }
            filename = f"siafi_amostra_{timestamp}.csv"

        elif resource == "compras":
            data = {
                "uasg": ["153978", "153979", "154357", "154358", "154359"],
                "id_contrato": ["2025/001", "2025/002", "2025/003", "2025/004", "2025/005"],
                "valor_total": [150000.00, 75000.50, 200000.00, 95000.75, 180000.25],
                "cnpj_contratada": [
                    "12345678000123",
                    "98765432000876",
                    "45678901000567",
                    "32109876000210",
                    "78901234000890",
                ],
                "objeto_contrato": [
                    "Serviços de TI",
                    "Manutenção Predial",
                    "Consultoria",
                    "Material de Escritório",
                    "Equipamentos",
                ],
                "data_assinatura": [
                    "2025-01-15",
                    "2025-02-20",
                    "2025-03-10",
                    "2025-04-05",
                    "2025-05-12",
                ],
                "modalidade": [
                    "Pregão Eletrônico",
                    "Concorrência",
                    "Tomada de Preços",
                    "Pregão Eletrônico",
                    "Dispensa",
                ],
            }
            filename = f"contratos_amostra_{timestamp}.csv"

        elif resource == "transferegov":
            data = {
                "codigo_siafi": ["153978", "153979", "154357", "154358", "154359"],
                "convenio": ["123456", "123457", "123458", "123459", "123460"],
                "valor_liberado": [150000.00, 75000.50, 200000.00, 95000.75, 180000.25],
                "data_liberacao": [
                    "2025-01-15",
                    "2025-02-20",
                    "2025-03-10",
                    "2025-04-05",
                    "2025-05-12",
                ],
                "beneficiario": [
                    "Município de São Paulo",
                    "Município do Rio de Janeiro",
                    "Município de Brasília",
                    "Município de Salvador",
                    "Município de Fortaleza",
                ],
                "uf": ["SP", "RJ", "DF", "BA", "CE"],
                "programa": [
                    "Educação Básica",
                    "Saúde da Família",
                    "Infraestrutura",
                    "Assistência Social",
                    "Meio Ambiente",
                ],
            }
            filename = f"convenios_amostra_{timestamp}.csv"

        else:
            logger.error(f"❌ Recurso não reconhecido para amostra: {resource}")
            return

        try:
            df = pd.DataFrame(data)
            output_file = self.output_dir / filename
            df.to_csv(output_file, index=False, encoding="utf-8")

            file_size = output_file.stat().st_size
            logger.info(f"✅ Dados de amostra criados: {output_file}")
            logger.info(f"   📊 {len(df)} registros, {file_size} bytes")

        except Exception as e:
            logger.error(f"❌ Erro ao criar dados de amostra: {e}")

    def acquire_all_data_sources(self) -> Dict[str, bool]:
        """
        Executa aquisição de dados de todas as fontes configuradas.

        Returns:
            Dicionário com status de sucesso para cada fonte
        """
        logger.info("🚀 === INICIANDO AQUISIÇÃO COMPLETA DE DADOS GOV-HUB ===")
        logger.info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        results = {}

        try:
            # SIAFI
            logger.info("\n" + "=" * 60)
            results["siafi"] = self.download_siafi_data()

            # Compras.gov.br
            logger.info("\n" + "=" * 60)
            results["compras"] = self.download_compras_data()

            # TransfereGov
            logger.info("\n" + "=" * 60)
            results["transferegov"] = self.download_transferegov_data()

        except KeyboardInterrupt:
            logger.warning("⚠️ Interrompido pelo usuário")
            return results
        except Exception as e:
            logger.error(f"❌ Erro crítico durante aquisição: {e}")
            return results

        # Relatório final
        logger.info("\n" + "=" * 60)
        logger.info("📊 === RELATÓRIO FINAL DE AQUISIÇÃO ===")

        total_sources = len(results)
        successful_sources = sum(results.values())

        for source, success in results.items():
            status = "✅ SUCESSO" if success else "❌ FALHOU"
            logger.info(f"   {source.upper()}: {status}")

        logger.info(
            f"\n📈 Taxa de sucesso: {successful_sources}/{total_sources} "
            f"({(successful_sources/total_sources)*100:.1f}%)"
        )

        if successful_sources > 0:
            logger.info("🎉 Aquisição concluída com dados disponíveis!")
        else:
            logger.warning(
                "⚠️ Nenhuma fonte teve sucesso, mas dados de amostra foram gerados"
            )

        # Listar arquivos gerados
        logger.info("\n📁 Arquivos gerados em data/raw/:")
        for file in sorted(self.output_dir.glob("*.csv")):
            file_size = file.stat().st_size / 1024
            logger.info(f"   📄 {file.name} ({file_size:.1f} KB)")

        return results


def main():
    """Função principal com interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Gov-Hub Data Acquirer - Sistema robusto de aquisição de dados governamentais"
    )

    parser.add_argument(
        "--source",
        choices=["siafi", "compras", "transferegov", "all"],
        default="all",
        help="Especifica a fonte de dados para download (padrão: all)",
    )

    parser.add_argument(
        "--config",
        default="config/config.json",
        help="Caminho para arquivo de configuração (padrão: config/config.json)",
    )

    args = parser.parse_args()

    try:
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("govhub_data_acquisition.log", encoding="utf-8"),
            ],
        )

        # Inicializar o Data Acquirer
        logger.info("Inicializando Gov-Hub Data Acquirer...")
        acquirer = GovHubDataAcquirer(config_path=args.config)

        # Executar downloads
        if args.source == "all":
            results = acquirer.acquire_all_data_sources()
            success = any(results.values())
        else:
            logger.info(f"Executando download específico: {args.source.upper()}")
            if args.source == "siafi":
                success = acquirer.download_siafi_data()
            elif args.source == "compras":
                success = acquirer.download_compras_data()
            elif args.source == "transferegov":
                success = acquirer.download_transferegov_data()

        if success:
            logger.info("🎉 Processo finalizado com sucesso!")
            return 0
        else:
            logger.warning("⚠️ Processo finalizado com dados de amostra")
            return 0

    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
