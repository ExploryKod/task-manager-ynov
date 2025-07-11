"""
Configuration globale pour pytest
Ajoute le répertoire du projet au PYTHONPATH pour permettre les imports depuis src/
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire racine du projet au Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# S'assurer que le répertoire src est dans le path
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path)) 