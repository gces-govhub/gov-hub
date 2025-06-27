"""
Gov-Hub Utilities Module
Módulo de utilitários para o sistema Gov-Hub.

Este módulo contém classes e funções utilitárias para validação,
logging, helpers e outras funcionalidades de suporte.

Módulos:
    validation: Sistema de validação completa do projeto
"""

__version__ = "1.0.0"
__author__ = "Gov-Hub Team"

from .validation import SystemValidator

__all__ = ["SystemValidator"]
