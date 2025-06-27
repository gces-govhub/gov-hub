"""
Gov-Hub Core Module
Módulos principais do sistema Gov-Hub.

Este módulo contém as funcionalidades centrais para aquisição, integração
e processamento de dados governamentais.

Módulos:
    acquisition: Aquisição robusta de dados governamentais
    integration: Integração padrão de dados
    processor: Processamento de arquivos grandes (SIAFI)
    advanced_integration: Integração avançada para dados em larga escala
"""

__version__ = "2.0.0"
__author__ = "Gov-Hub Team"

from .acquisition import GovHubDataAcquirer
from .integration import DataIntegrator
from .processor import SiafiLargeFileProcessor
from .advanced_integration import AdvancedDataIntegrator

__all__ = [
    "GovHubDataAcquirer",
    "DataIntegrator",
    "SiafiLargeFileProcessor", 
    "AdvancedDataIntegrator",
]
