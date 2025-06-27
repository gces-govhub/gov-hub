#!/usr/bin/env python3
"""
Gov-Hub Validation Module
Módulo para validação completa do sistema Gov-Hub.

Este módulo fornece validações abrangentes para garantir que todos os componentes
do sistema estejam funcionando corretamente antes da execução.

Classes:
    SystemValidator: Validador principal do sistema
"""

import json
import logging
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

logger = logging.getLogger(__name__)


class SystemValidator:
    """
    Validador principal do sistema Gov-Hub.
    
    Performs comprehensive system validation including configuration,
    dependencies, file structure, and module imports.
    """
    
    def __init__(self, base_dir: str = "."):
        """
        Inicializa o validador do sistema.
        
        Args:
            base_dir: Diretório base do projeto
        """
        self.base_dir = Path(base_dir)
        self.required_files = [
            "src/govhub/core/acquisition.py",
            "src/govhub/core/integration.py", 
            "config/config.json",
            "requirements.txt",
        ]
        self.required_dirs = [
            "data",
            "data/raw", 
            "data/processed",
            "src/govhub",
            "src/govhub/core",
            "scripts"
        ]
        
        logger.info("SystemValidator inicializado")
        logger.info(f"Diretório base: {self.base_dir.absolute()}")

    def validate_project_structure(self) -> bool:
        """
        Valida se a estrutura de arquivos e diretórios está correta.
        
        Returns:
            True se a estrutura está válida, False caso contrário
        """
        logger.info("🔍 Validando estrutura do projeto...")
        
        structure_valid = True

        # Verificar arquivos essenciais
        for file_path in self.required_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                logger.error(f"❌ Arquivo não encontrado: {file_path}")
                structure_valid = False
            else:
                logger.info(f"✅ {file_path}")

        # Verificar e criar diretórios se necessário
        for dir_path in self.required_dirs:
            full_path = self.base_dir / dir_path
            if not full_path.exists():
                logger.warning(f"⚠️ Diretório não existe, criando: {dir_path}")
                full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ {dir_path}/")

        if structure_valid:
            logger.info("✅ Estrutura do projeto válida")
        else:
            logger.error("❌ Estrutura do projeto incompleta")

        return structure_valid

    def validate_configuration_file(self) -> bool:
        """
        Valida se o arquivo de configuração está correto.
        
        Returns:
            True se a configuração é válida, False caso contrário
        """
        logger.info("🔍 Validando arquivo de configuração...")

        config_path = self.base_dir / "config" / "config.json"
        if not config_path.exists():
            logger.error("❌ Arquivo config/config.json não encontrado")
            return False

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # Verificar estrutura principal
            required_sections = ["data_sources", "download_settings", "file_settings"]
            for section in required_sections:
                if section not in config:
                    logger.error(f"❌ Seção obrigatória não encontrada: {section}")
                    return False

            # Verificar fontes de dados
            required_sources = ["siafi", "compras", "transferegov"]
            for source in required_sources:
                if source not in config["data_sources"]:
                    logger.error(f"❌ Fonte de dados não configurada: {source}")
                    return False

                if "urls" not in config["data_sources"][source]:
                    logger.error(f"❌ URLs não configuradas para: {source}")
                    return False

            logger.info("✅ Arquivo de configuração válido")
            return True

        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro no JSON de configuração: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao validar configuração: {e}")
            return False

    def validate_python_dependencies(self) -> bool:
        """
        Valida se todas as dependências Python estão instaladas.
        
        Returns:
            True se todas as dependências estão disponíveis, False caso contrário
        """
        logger.info("🔍 Validando dependências Python...")

        required_modules = [
            "requests", "pandas", "numpy", "json", "zipfile", 
            "pathlib", "csv", "logging", "datetime"
        ]

        missing_modules = []

        for module in required_modules:
            try:
                __import__(module)
                logger.debug(f"✅ {module}")
            except ImportError:
                logger.error(f"❌ {module} não encontrado")
                missing_modules.append(module)

        if missing_modules:
            logger.error(f"❌ Módulos faltando: {', '.join(missing_modules)}")
            logger.info("💡 Execute: pip install -r requirements.txt")
            return False

        logger.info("✅ Todas as dependências estão instaladas")
        return True

    def test_core_modules_import(self) -> bool:
        """
        Testa se os módulos principais podem ser importados.
        
        Returns:
            True se os módulos podem ser importados, False caso contrário
        """
        logger.info("🔍 Testando importação dos módulos principais...")

        try:
            # Adicionar o diretório src ao path
            src_path = str(self.base_dir / "src")
            if src_path not in sys.path:
                sys.path.insert(0, src_path)

            # Tentar importar módulos principais
            from govhub.core.acquisition import GovHubDataAcquirer
            from govhub.core.integration import DataIntegrator
            
            logger.info("✅ Módulo de aquisição importado")
            logger.info("✅ Módulo de integração importado")

            # Testar instanciação básica
            try:
                acquirer = GovHubDataAcquirer()
                integrator = DataIntegrator()
                logger.info("✅ Módulos podem ser instanciados")
                return True
            except Exception as e:
                logger.error(f"❌ Erro ao instanciar módulos: {e}")
                return False

        except ImportError as e:
            logger.error(f"❌ Erro ao importar módulos principais: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Erro inesperado na importação: {e}")
            return False

    def test_configuration_loading(self) -> bool:
        """
        Executa teste de carregamento de configuração.
        
        Returns:
            True se a configuração pode ser carregada, False caso contrário
        """
        logger.info("🔍 Testando carregamento de configuração...")

        try:
            # Adicionar o diretório src ao path
            src_path = str(self.base_dir / "src")
            if src_path not in sys.path:
                sys.path.insert(0, src_path)

            from govhub.core.acquisition import GovHubDataAcquirer

            # Criar instância e testar configuração
            acquirer = GovHubDataAcquirer()

            # Verificar se configurações foram carregadas
            if hasattr(acquirer, "config") and acquirer.config:
                logger.info("✅ Configurações carregadas com sucesso")

                # Verificar diretórios
                if acquirer.output_dir.exists() and acquirer.temp_dir.exists():
                    logger.info("✅ Diretórios de trabalho criados")
                    return True
                else:
                    logger.error("❌ Diretórios de trabalho não foram criados")
                    return False
            else:
                logger.error("❌ Configurações não foram carregadas")
                return False

        except Exception as e:
            logger.error(f"❌ Erro no teste de configuração: {e}")
            return False

    def validate_scripts_directory(self) -> bool:
        """
        Valida se o diretório de scripts está configurado corretamente.
        
        Returns:
            True se o diretório de scripts está válido, False caso contrário
        """
        logger.info("🔍 Validando diretório de scripts...")
        
        scripts_dir = self.base_dir / "scripts"
        if not scripts_dir.exists():
            logger.warning("⚠️ Diretório scripts não existe, criando...")
            scripts_dir.mkdir(parents=True, exist_ok=True)

        # Verificar se há scripts PowerShell que deveriam estar em scripts/
        root_ps1_files = list(self.base_dir.glob("*.ps1"))
        if root_ps1_files:
            logger.info(f"ℹ️ Encontrados {len(root_ps1_files)} scripts PowerShell no diretório raiz")
            logger.info("💡 Considere mover scripts para o diretório scripts/")

        logger.info("✅ Diretório de scripts validado")
        return True

    def run_comprehensive_validation(self) -> Dict[str, bool]:
        """
        Executa validação completa do sistema.
        
        Returns:
            Dicionário com resultados de cada teste
        """
        logger.info("🚀 === Iniciando Validação Completa do Sistema ===")

        validation_tests = [
            ("Estrutura do Projeto", self.validate_project_structure),
            ("Arquivo de Configuração", self.validate_configuration_file),
            ("Dependências Python", self.validate_python_dependencies),
            ("Importação de Módulos", self.test_core_modules_import),
            ("Carregamento de Configuração", self.test_configuration_loading),
            ("Diretório de Scripts", self.validate_scripts_directory),
        ]

        results = {}

        for test_name, test_func in validation_tests:
            logger.info(f"\n--- {test_name} ---")
            try:
                result = test_func()
                results[test_name] = result
            except Exception as e:
                logger.error(f"❌ Erro inesperado em {test_name}: {e}")
                results[test_name] = False

        return results

    def generate_validation_report(self, results: Dict[str, bool]) -> str:
        """
        Gera relatório detalhado da validação.
        
        Args:
            results: Resultados dos testes de validação
            
        Returns:
            Relatório em formato texto
        """
        logger.info("\n" + "=" * 60)
        logger.info("📊 === RELATÓRIO DE VALIDAÇÃO ===")

        passed = sum(1 for result in results.values() if result)
        total = len(results)

        report_lines = [
            "=== RELATÓRIO DE VALIDAÇÃO DO SISTEMA GOV-HUB ===",
            f"Data/Hora: {Path(__file__).stat().st_mtime}",
            "",
            "📊 RESULTADOS DOS TESTES:",
        ]

        for test_name, result in results.items():
            status = "✅ PASSOU" if result else "❌ FALHOU"
            logger.info(f"  {test_name}: {status}")
            report_lines.append(f"   • {test_name}: {status}")

        report_lines.extend([
            "",
            f"📈 Resumo: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)",
            "",
        ])

        if passed == total:
            logger.info("🎉 SISTEMA TOTALMENTE VALIDADO!")
            logger.info("💡 Sistema pronto para execução")
            report_lines.extend([
                "🎉 STATUS: SISTEMA TOTALMENTE VALIDADO",
                "✅ Todos os testes passaram com sucesso",
                "💡 O sistema está pronto para execução",
                "",
                "🚀 PRÓXIMOS PASSOS:",
                "   1. Execute: python -m govhub.core.acquisition --source all",
                "   2. Execute: python -m govhub.core.integration",
                "   3. Verifique os resultados em data/processed/",
            ])
        else:
            logger.error("⚠️ Sistema não está totalmente validado")
            logger.error("📋 Corrija os problemas identificados antes de continuar")
            report_lines.extend([
                "⚠️ STATUS: SISTEMA PARCIALMENTE VALIDADO",
                "❌ Alguns testes falharam",
                "📋 Corrija os problemas identificados antes de continuar",
                "",
                "🔧 AÇÕES RECOMENDADAS:",
                "   1. Verifique se todos os arquivos estão presentes",
                "   2. Execute: pip install -r requirements.txt",
                "   3. Verifique o arquivo config/config.json",
                "   4. Execute a validação novamente",
            ])

        return "\n".join(report_lines)


def main():
    """Função principal para execução standalone."""
    import sys
    from datetime import datetime
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
    )

    try:
        validator = SystemValidator()
        results = validator.run_comprehensive_validation()
        
        # Gerar relatório
        report = validator.generate_validation_report(results)
        
        # Salvar relatório
        report_path = Path("validation_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"📄 Relatório salvo: {report_path}")
        
        # Retornar código de saída apropriado
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        return 0 if passed == total else 1

    except Exception as e:
        logger.error(f"Erro crítico na validação: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
