#!/usr/bin/env python3
"""
Validador Completo da PoC SIAFI - Gov-Hub
Script para validar e testar todos os componentes da PoC.
"""

import sys
from pathlib import Path
import logging
import subprocess
import importlib

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class PocValidator:
    """Validador completo da PoC SIAFI."""
    
    def __init__(self):
        self.base_dir = Path(".")
        self.results = []
    
    def validate_dependencies(self):
        """Valida se todas as dependências estão instaladas."""
        logger.info("🔍 Validando dependências...")
        
        required_packages = [
            'pandas', 'numpy', 'requests', 
            'pathlib', 'logging', 'json'
        ]
        
        missing = []
        for package in required_packages:
            try:
                importlib.import_module(package)
                logger.info(f"  ✅ {package}")
            except ImportError:
                missing.append(package)
                logger.error(f"  ❌ {package}")
        
        if missing:
            self.results.append(f"❌ Dependências faltando: {', '.join(missing)}")
            return False
        else:
            self.results.append("✅ Todas as dependências estão instaladas")
            return True
    
    def validate_structure(self):
        """Valida a estrutura de diretórios."""
        logger.info("🔍 Validando estrutura de diretórios...")
        
        required_dirs = [
            "data",
            "data/poc_siafi",
            "data/poc_siafi/dados_brutos",
            "data/poc_siafi/dados_processados", 
            "data/poc_siafi/relatorios"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            path = Path(dir_path)
            if path.exists():
                logger.info(f"  ✅ {dir_path}")
            else:
                missing_dirs.append(dir_path)
                logger.error(f"  ❌ {dir_path}")
        
        if missing_dirs:
            self.results.append(f"❌ Diretórios faltando: {', '.join(missing_dirs)}")
            return False
        else:
            self.results.append("✅ Estrutura de diretórios correta")
            return True
    
    def validate_scripts(self):
        """Valida se todos os scripts principais existem."""
        logger.info("🔍 Validando scripts...")
        
        required_scripts = [
            "organize_siafi.py",
            "run_siafi_poc.py", 
            "generate_realistic_siafi.py",
            "acquire_real_siafi.py"
        ]
        
        missing_scripts = []
        for script in required_scripts:
            path = Path(script)
            if path.exists():
                logger.info(f"  ✅ {script}")
            else:
                missing_scripts.append(script)
                logger.error(f"  ❌ {script}")
        
        if missing_scripts:
            self.results.append(f"❌ Scripts faltando: {', '.join(missing_scripts)}")
            return False
        else:
            self.results.append("✅ Todos os scripts estão presentes")
            return True
    
    def test_data_generation(self):
        """Testa a geração de dados."""
        logger.info("🔍 Testando geração de dados...")
        
        try:
            # Importar e testar gerador
            from generate_realistic_siafi import SiafiDataGenerator
            
            generator = SiafiDataGenerator()
            test_file = generator.generate_realistic_siafi_data(num_records=100)
            
            if test_file.exists():
                logger.info(f"  ✅ Arquivo gerado: {test_file.name}")
                self.results.append("✅ Geração de dados funcionando")
                return True
            else:
                logger.error("  ❌ Arquivo não foi criado")
                self.results.append("❌ Falha na geração de dados")
                return False
                
        except Exception as e:
            logger.error(f"  ❌ Erro na geração: {e}")
            self.results.append(f"❌ Erro na geração de dados: {e}")
            return False
    
    def test_organization(self):
        """Testa a organização de dados."""
        logger.info("🔍 Testando organização de dados...")
        
        try:
            from organize_siafi import organize_existing_siafi_data
            
            organize_existing_siafi_data()
            
            # Verificar se arquivos foram criados
            raw_dir = Path("data/poc_siafi/dados_brutos")
            files = list(raw_dir.glob("*.csv"))
            
            if files:
                logger.info(f"  ✅ {len(files)} arquivos organizados")
                self.results.append("✅ Organização de dados funcionando")
                return True
            else:
                logger.error("  ❌ Nenhum arquivo organizado")
                self.results.append("❌ Falha na organização")
                return False
                
        except Exception as e:
            logger.error(f"  ❌ Erro na organização: {e}")
            self.results.append(f"❌ Erro na organização: {e}")
            return False
    
    def test_poc_execution(self):
        """Testa a execução da PoC."""
        logger.info("🔍 Testando execução da PoC...")
        
        try:
            from run_siafi_poc import run_siafi_poc
            
            result = run_siafi_poc()
            
            if result is not False:
                logger.info("  ✅ PoC executada com sucesso")
                self.results.append("✅ Execução da PoC funcionando")
                return True
            else:
                logger.error("  ❌ PoC retornou falha")
                self.results.append("❌ Falha na execução da PoC")
                return False
                
        except Exception as e:
            logger.error(f"  ❌ Erro na PoC: {e}")
            self.results.append(f"❌ Erro na execução da PoC: {e}")
            return False
    
    def check_gitignore(self):
        """Verifica se o .gitignore está configurado corretamente."""
        logger.info("🔍 Verificando .gitignore...")
        
        gitignore_path = Path(".gitignore")
        if not gitignore_path.exists():
            self.results.append("❌ Arquivo .gitignore não encontrado")
            return False
        
        content = gitignore_path.read_text(encoding='utf-8')
        
        required_patterns = [
            "data/poc_siafi/dados_brutos/*.csv",
            "data/poc_siafi/dados_brutos/*.json",
            "data/poc_siafi/dados_processados/*.csv",
            "data/poc_siafi/relatorios/*.txt"
        ]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            logger.error(f"  ❌ Padrões faltando no .gitignore: {missing_patterns}")
            self.results.append("❌ .gitignore incompleto")
            return False
        else:
            logger.info("  ✅ .gitignore configurado corretamente")
            self.results.append("✅ .gitignore configurado corretamente")
            return True
    
    def generate_validation_report(self):
        """Gera relatório final de validação."""
        report_path = Path("data/poc_siafi/relatorios/relatorio_validacao_completa.txt")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE VALIDAÇÃO COMPLETA - POC SIAFI\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Data da Validação: {logging.Formatter().formatTime(logging.LogRecord('', 0, '', 0, '', (), None))}\n\n")
            
            f.write("RESULTADOS DOS TESTES:\n")
            f.write("-" * 40 + "\n")
            
            passed = 0
            total = len(self.results)
            
            for result in self.results:
                f.write(f"{result}\n")
                if result.startswith("✅"):
                    passed += 1
            
            f.write(f"\nRESUMO FINAL:\n")
            f.write("-" * 40 + "\n")
            f.write(f"✅ Testes Aprovados: {passed}/{total}\n")
            f.write(f"❌ Testes Falhados: {total - passed}/{total}\n")
            f.write(f"📊 Taxa de Sucesso: {(passed/total)*100:.1f}%\n\n")
            
            if passed == total:
                f.write("🎉 VALIDAÇÃO COMPLETA: TODOS OS TESTES APROVADOS!\n")
                f.write("✅ A PoC SIAFI está 100% funcional e pronta para uso.\n")
            else:
                f.write("⚠️ VALIDAÇÃO PARCIAL: Alguns testes falharam.\n")
                f.write("🔧 Verifique os itens marcados com ❌ e corrija antes de prosseguir.\n")
        
        logger.info(f"📋 Relatório de validação salvo: {report_path.name}")
        return passed == total
    
    def run_complete_validation(self):
        """Executa validação completa."""
        logger.info("🚀 === INICIANDO VALIDAÇÃO COMPLETA DA POC SIAFI ===")
        
        tests = [
            ("Dependências", self.validate_dependencies),
            ("Estrutura", self.validate_structure),
            ("Scripts", self.validate_scripts),
            ("GitIgnore", self.check_gitignore),
            ("Organização", self.test_organization),
            ("Geração de Dados", self.test_data_generation),
            ("Execução da PoC", self.test_poc_execution)
        ]
        
        passed_tests = 0
        
        for test_name, test_func in tests:
            logger.info(f"\n🔍 === TESTE: {test_name.upper()} ===")
            try:
                if test_func():
                    passed_tests += 1
                    logger.info(f"✅ {test_name}: APROVADO")
                else:
                    logger.error(f"❌ {test_name}: FALHADO")
            except Exception as e:
                logger.error(f"❌ {test_name}: ERRO - {e}")
                self.results.append(f"❌ {test_name}: Erro durante execução - {e}")
        
        # Gerar relatório final
        all_passed = self.generate_validation_report()
        
        logger.info(f"\n🎯 === VALIDAÇÃO CONCLUÍDA ===")
        logger.info(f"📊 Testes Aprovados: {passed_tests}/{len(tests)}")
        
        if all_passed:
            logger.info("🎉 SUCESSO TOTAL: PoC SIAFI 100% VALIDADA!")
            return True
        else:
            logger.error("⚠️ VALIDAÇÃO PARCIAL: Alguns componentes precisam de correção.")
            return False

def main():
    """Função principal."""
    validator = PocValidator()
    success = validator.run_complete_validation()
    
    if success:
        print("\n🎉 PoC SIAFI TOTALMENTE VALIDADA E FUNCIONANDO!")
        print("✅ Todos os componentes estão operacionais.")
        print("🚀 Pronta para demonstração e uso em produção!")
    else:
        print("\n⚠️ PoC SIAFI com alguns problemas detectados.")
        print("🔧 Verifique o relatório de validação para detalhes.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
