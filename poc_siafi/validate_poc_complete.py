#!/usr/bin/env python3
"""
Validador Completo da PoC SIAFI - Gov-Hub
Script para validar toda a infraestrutura e funcionalidade da PoC.
"""

import sys
import subprocess
import importlib
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class PocValidator:
    """Validador completo da PoC SIAFI."""
    
    def __init__(self):
        self.base_dir = Path("data/poc_siafi")
        self.results = []
        self.errors = []
    
    def log_result(self, test_name: str, status: bool, message: str):
        """Registra resultado de um teste."""
        symbol = "✅" if status else "❌"
        result = f"{symbol} {test_name}: {message}"
        print(result)
        self.results.append((test_name, status, message))
        if not status:
            self.errors.append(result)
    
    def validate_environment(self):
        """Valida o ambiente Python e dependências."""
        print("\n🔧 VALIDANDO AMBIENTE")
        print("=" * 50)
        
        # Verificar versão do Python
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.log_result("Python Version", True, f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            self.log_result("Python Version", False, f"Python {python_version.major}.{python_version.minor} (mínimo: 3.8)")
        
        # Verificar dependências críticas
        critical_deps = ['pandas', 'requests', 'numpy', 'pathlib']
        for dep in critical_deps:
            try:
                importlib.import_module(dep)
                self.log_result(f"Dependência {dep}", True, "Instalada")
            except ImportError:
                self.log_result(f"Dependência {dep}", False, "Não encontrada")
        
        # Verificar arquivo requirements.txt
        req_file = Path("requirements.txt")
        if req_file.exists():
            self.log_result("Requirements.txt", True, "Presente")
        else:
            self.log_result("Requirements.txt", False, "Não encontrado")
    
    def validate_structure(self):
        """Valida a estrutura de diretórios da PoC."""
        print("\n📁 VALIDANDO ESTRUTURA DE DIRETÓRIOS")
        print("=" * 50)
        
        required_dirs = [
            "data/poc_siafi",
            "data/poc_siafi/dados_brutos",
            "data/poc_siafi/dados_processados", 
            "data/poc_siafi/relatorios"
        ]
        
        for dir_path in required_dirs:
            path = Path(dir_path)
            if path.exists() and path.is_dir():
                self.log_result(f"Diretório {dir_path}", True, "Existe")
            else:
                self.log_result(f"Diretório {dir_path}", False, "Não encontrado")
        
        # Verificar arquivos .gitkeep
        gitkeep_files = [
            "data/poc_siafi/dados_brutos/.gitkeep",
            "data/poc_siafi/dados_processados/.gitkeep",
            "data/poc_siafi/relatorios/.gitkeep"
        ]
        
        for gitkeep in gitkeep_files:
            path = Path(gitkeep)
            if path.exists():
                self.log_result(f"GitKeep {gitkeep}", True, "Presente")
            else:
                self.log_result(f"GitKeep {gitkeep}", False, "Ausente")
    
    def validate_scripts(self):
        """Valida a presença e sintaxe dos scripts principais."""
        print("\n🐍 VALIDANDO SCRIPTS")
        print("=" * 50)
        
        scripts = [
            "organize_siafi.py",
            "run_siafi_poc.py",
            "collect_real_siafi.py",
            "demo_api_real.py"
        ]
        
        for script in scripts:
            script_path = Path(script)
            if script_path.exists():
                self.log_result(f"Script {script}", True, "Existe")
                
                # Testar sintaxe
                try:
                    with open(script_path, 'r', encoding='utf-8') as f:
                        compile(f.read(), script, 'exec')
                    self.log_result(f"Sintaxe {script}", True, "Válida")
                except SyntaxError as e:
                    self.log_result(f"Sintaxe {script}", False, f"Erro: {e}")
            else:
                self.log_result(f"Script {script}", False, "Não encontrado")
    
    def validate_git_setup(self):
        """Valida configuração do Git."""
        print("\n📋 VALIDANDO CONFIGURAÇÃO GIT")
        print("=" * 50)
        
        # Verificar .gitignore
        gitignore = Path(".gitignore")
        if gitignore.exists():
            self.log_result("Arquivo .gitignore", True, "Presente")
            
            # Verificar se ignora dados
            with open(gitignore, 'r', encoding='utf-8') as f:
                content = f.read()
                if "data/poc_siafi/dados_brutos/*.csv" in content:
                    self.log_result("GitIgnore - Dados CSV", True, "Configurado")
                else:
                    self.log_result("GitIgnore - Dados CSV", False, "Não configurado")
                
                if "*.log" in content:
                    self.log_result("GitIgnore - Logs", True, "Configurado")
                else:
                    self.log_result("GitIgnore - Logs", False, "Não configurado")
        else:
            self.log_result("Arquivo .gitignore", False, "Não encontrado")
        
        # Verificar .env.example
        env_example = Path(".env.example")
        if env_example.exists():
            self.log_result("Arquivo .env.example", True, "Presente")
        else:
            self.log_result("Arquivo .env.example", False, "Não encontrado")
    
    def validate_functionality(self):
        """Valida funcionalidade básica executando scripts."""
        print("\n⚡ VALIDANDO FUNCIONALIDADE")
        print("=" * 50)
        
        # Testar organização
        try:
            result = subprocess.run([sys.executable, "organize_siafi.py"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.log_result("Execução organize_siafi.py", True, "Sucesso")
            else:
                self.log_result("Execução organize_siafi.py", False, f"Erro: {result.stderr[:100]}")
        except Exception as e:
            self.log_result("Execução organize_siafi.py", False, f"Exceção: {e}")
        
        # Testar PoC principal
        try:
            result = subprocess.run([sys.executable, "run_siafi_poc.py"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.log_result("Execução run_siafi_poc.py", True, "Sucesso")
            else:
                self.log_result("Execução run_siafi_poc.py", False, f"Erro: {result.stderr[:100]}")
        except Exception as e:
            self.log_result("Execução run_siafi_poc.py", False, f"Exceção: {e}")
    
    def validate_data_presence(self):
        """Valida presença de dados após execução."""
        print("\n📊 VALIDANDO DADOS GERADOS")
        print("=" * 50)
        
        # Verificar dados organizados
        raw_files = list(Path("data/poc_siafi/dados_brutos").glob("*.csv"))
        if raw_files:
            self.log_result("Dados Brutos", True, f"{len(raw_files)} arquivos encontrados")
        else:
            self.log_result("Dados Brutos", False, "Nenhum arquivo CSV encontrado")
        
        # Verificar dados processados
        processed_files = list(Path("data/poc_siafi/dados_processados").glob("*.csv"))
        if processed_files:
            self.log_result("Dados Processados", True, f"{len(processed_files)} arquivos encontrados")
        else:
            self.log_result("Dados Processados", False, "Nenhum arquivo encontrado")
        
        # Verificar relatórios
        report_files = list(Path("data/poc_siafi/relatorios").glob("*.txt"))
        if report_files:
            self.log_result("Relatórios", True, f"{len(report_files)} relatórios encontrados")
        else:
            self.log_result("Relatórios", False, "Nenhum relatório encontrado")
    
    def generate_final_report(self):
        """Gera relatório final da validação."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = Path(f"data/poc_siafi/relatorios/validacao_completa_{timestamp}.txt")
        
        passed_tests = sum(1 for _, status, _ in self.results if status)
        total_tests = len(self.results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE VALIDAÇÃO COMPLETA - POC SIAFI GOV-HUB\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"🕒 Data da Validação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"🎯 Escopo: Validação completa da PoC SIAFI\n")
            f.write(f"📊 Taxa de Sucesso: {success_rate:.1f}% ({passed_tests}/{total_tests})\n\n")
            
            f.write("📋 RESULTADOS DETALHADOS:\n")
            f.write("-" * 60 + "\n")
            for test_name, status, message in self.results:
                symbol = "✅" if status else "❌"
                f.write(f"{symbol} {test_name}: {message}\n")
            
            if self.errors:
                f.write(f"\n❌ PROBLEMAS ENCONTRADOS ({len(self.errors)}):\n")
                f.write("-" * 60 + "\n")
                for error in self.errors:
                    f.write(f"{error}\n")
            
            f.write(f"\n🎯 CONCLUSÃO:\n")
            f.write("-" * 60 + "\n")
            if success_rate >= 90:
                f.write("✅ PoC SIAFI VALIDADA COM SUCESSO!\n")
                f.write("🚀 Sistema pronto para uso em produção.\n")
            elif success_rate >= 75:
                f.write("⚠️ PoC SIAFI FUNCIONAL COM RESSALVAS\n")
                f.write("🔧 Corrija os problemas identificados para melhor performance.\n")
            else:
                f.write("❌ PoC SIAFI REQUER CORREÇÕES\n")
                f.write("🛠️ Múltiplos problemas identificados. Revisar configuração.\n")
            
            f.write(f"\n📈 PRÓXIMOS PASSOS:\n")
            f.write("-" * 60 + "\n")
            f.write("1. Configurar chave da API do Portal da Transparência\n")
            f.write("2. Executar coleta de dados reais: python collect_real_siafi.py\n")
            f.write("3. Analisar dados coletados\n")
            f.write("4. Desenvolver análises específicas conforme necessidade\n")
            f.write("5. Documentar insights e descobertas\n")
        
        logger.info(f"📋 Relatório de validação salvo: {report_file}")
        return report_file, success_rate
    
    def run_complete_validation(self):
        """Executa validação completa da PoC."""
        print("🏛️ GOV-HUB PoC SIAFI - VALIDAÇÃO COMPLETA")
        print("=" * 60)
        
        # Executar todas as validações
        self.validate_environment()
        self.validate_structure()
        self.validate_scripts()
        self.validate_git_setup()
        self.validate_functionality()
        self.validate_data_presence()
        
        # Gerar relatório final
        report_file, success_rate = self.generate_final_report()
        
        # Mostrar resumo
        print(f"\n📊 RESUMO FINAL")
        print("=" * 30)
        print(f"Taxa de Sucesso: {success_rate:.1f}%")
        print(f"Testes Executados: {len(self.results)}")
        print(f"Problemas: {len(self.errors)}")
        print(f"Relatório: {report_file.name}")
        
        if success_rate >= 90:
            print("\n🎉 PoC SIAFI VALIDADA COM SUCESSO!")
            print("✅ Sistema pronto para coleta de dados reais.")
        else:
            print(f"\n⚠️ PoC precisa de ajustes ({len(self.errors)} problemas)")
            print("🔧 Verifique o relatório para detalhes.")

def main():
    """Função principal."""
    validator = PocValidator()
    validator.run_complete_validation()

if __name__ == "__main__":
    main()
