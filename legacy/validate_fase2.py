#!/usr/bin/env python3
"""
Validador da Fase 2 - Gov-Hub
Script para validar se o sistema de aquisição real está funcionando corretamente.
"""

import json
import logging
import sys
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def validate_config_file():
    """Valida se o arquivo de configuração está correto."""
    logger.info("🔍 Validando arquivo de configuração...")

    config_path = Path("config.json")
    if not config_path.exists():
        logger.error("❌ Arquivo config.json não encontrado")
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


def validate_dependencies():
    """Valida se todas as dependências estão instaladas."""
    logger.info("🔍 Validando dependências Python...")

    required_modules = ["requests", "pandas", "numpy", "json", "zipfile", "pathlib"]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✅ {module}")
        except ImportError:
            logger.error(f"❌ {module} não encontrado")
            missing_modules.append(module)

    if missing_modules:
        logger.error(f"❌ Módulos faltando: {', '.join(missing_modules)}")
        logger.info("💡 Execute: pip install -r requirements.txt")
        return False

    logger.info("✅ Todas as dependências estão instaladas")
    return True


def validate_file_structure():
    """Valida se a estrutura de arquivos está correta."""
    logger.info("🔍 Validando estrutura de arquivos...")

    required_files = [
        "data_acquirer.py",
        "integrate_data_simple.py",
        "config.json",
        "requirements.txt",
    ]

    required_dirs = ["data", "data/raw", "data/processed"]

    # Verificar arquivos
    for file_path in required_files:
        if not Path(file_path).exists():
            logger.error(f"❌ Arquivo não encontrado: {file_path}")
            return False
        logger.info(f"✅ {file_path}")

    # Verificar e criar diretórios se necessário
    for dir_path in required_dirs:
        dir_obj = Path(dir_path)
        if not dir_obj.exists():
            logger.warning(f"⚠️ Diretório não existe, criando: {dir_path}")
            dir_obj.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ {dir_path}/")

    logger.info("✅ Estrutura de arquivos válida")
    return True


def test_data_acquirer_import():
    """Testa se o data_acquirer.py pode ser importado."""
    logger.info("🔍 Testando importação do data_acquirer...")

    try:
        sys.path.insert(0, str(Path.cwd()))

        # Tentar importar o módulo
        import data_acquirer

        # Verificar se a classe principal existe
        if hasattr(data_acquirer, "GovHubDataAcquirer"):
            logger.info("✅ Classe GovHubDataAcquirer encontrada")

            # Tentar instanciar (sem executar downloads)
            try:
                data_acquirer.GovHubDataAcquirer()
                logger.info("✅ data_acquirer pode ser instanciado")
                return True
            except Exception as e:
                logger.error(f"❌ Erro ao instanciar data_acquirer: {e}")
                return False
        else:
            logger.error("❌ Classe GovHubDataAcquirer não encontrada")
            return False

    except ImportError as e:
        logger.error(f"❌ Erro ao importar data_acquirer: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        return False


def test_dry_run():
    """Executa um teste de configuração sem downloads."""
    logger.info("🔍 Executando teste de configuração...")

    try:
        sys.path.insert(0, str(Path.cwd()))
        import data_acquirer

        # Criar instância
        acquirer = data_acquirer.GovHubDataAcquirer()

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


def main():
    """Executa validação completa do sistema."""
    logger.info("🚀 === Iniciando Validação da Fase 2 Gov-Hub ===")

    tests = [
        ("Estrutura de Arquivos", validate_file_structure),
        ("Arquivo de Configuração", validate_config_file),
        ("Dependências Python", validate_dependencies),
        ("Importação Data Acquirer", test_data_acquirer_import),
        ("Teste de Configuração", test_dry_run),
    ]

    results = []

    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))

    # Relatório final
    logger.info("\n" + "=" * 60)
    logger.info("📊 === RELATÓRIO DE VALIDAÇÃO ===")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        logger.info(f"  {test_name}: {status}")

    logger.info(
        f"\n📈 Resultado: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)"
    )

    if passed == total:
        logger.info("🎉 SISTEMA PRONTO PARA FASE 2!")
        logger.info("💡 Execute: python data_acquirer.py --source all --verbose")
        return 0
    else:
        logger.error("⚠️ Sistema não está pronto. Corrija os problemas acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
