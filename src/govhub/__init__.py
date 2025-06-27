"""
Gov-Hub: Plataforma Modular de Integração de Dados Governamentais Brasileiros

Sistema profissional para aquisição, processamento e integração de dados de fontes
governamentais brasileiras (SIAFI, Compras.gov.br, TransfereGov).

Arquitetura Refatorada:
    - core/: Módulos principais (acquisition, integration, processor, advanced_integration)
    - utils/: Utilitários e validadores (validation)
    
Características:
    ✅ Estrutura modular e escalável
    ✅ Tratamento robusto de dados grandes
    ✅ Sistema completo de validação
    ✅ Integração avançada de múltiplas fontes
    ✅ Logging detalhado e relatórios abrangentes
"""

__version__ = "2.0.0"
__author__ = "Gov-Hub Team"
__description__ = "Plataforma Modular de Integração de Dados Governamentais"

# Importações principais para facilitar o uso
from .core.acquisition import GovHubDataAcquirer
from .core.integration import DataIntegrator
from .core.processor import SiafiLargeFileProcessor
from .core.advanced_integration import AdvancedDataIntegrator
from .utils.validation import SystemValidator

__all__ = [
    "GovHubDataAcquirer",
    "DataIntegrator", 
    "SiafiLargeFileProcessor",
    "AdvancedDataIntegrator",
    "SystemValidator"
]
