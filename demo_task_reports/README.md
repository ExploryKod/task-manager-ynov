# Demo Task Reports

Ce dossier contient les rapports de tâches générés par les scripts de démonstration, organisés par format.

## Structure des dossiers

```
demo_task_reports/
├── json/    # Rapports au format JSON
├── xml/     # Rapports au format XML  
└── xlsx/    # Rapports au format Excel
```

## Fichiers générés

### 📄 Format JSON (`json/`)
- `demo_tasks.json` - Données du script de démonstration principal
- `example_tasks.json` - Données du script d'exemple simple
- `export_demo_tasks.json` - Export complet avec statistiques
- `export_demo_tasks_no_stats.json` - Export sans statistiques

### 📄 Format XML (`xml/`)
- `rapport_tasks.xml` - Rapport simple avec statistiques
- `export_demo_tasks.xml` - Export complet avec structure hiérarchique

### 📊 Format Excel (`xlsx/`)
- `rapport_tasks.xlsx` - Rapport simple avec onglets Tasks et Statistics
- `export_demo_tasks.xlsx` - Export complet avec formatage professionnel

## Scripts qui génèrent ces fichiers

- `demo.py` - Script de démonstration principal (génère les fichiers JSON de base)
- `demo_export_simple.py` - Exemple simple d'export multi-format
- `demo_export.py` - Démonstration complète avec tous les formats

## Utilisation

Pour générer les rapports, exécutez :

```bash
# Démonstration principale
python demo.py

# Export simple
python demo_export_simple.py
# ou
make demo-export

# Export complet
python demo_export.py
```

## Visualisation

Pour ouvrir les fichiers :

```bash
# JSON
cat demo_task_reports/json/export_demo_tasks.json

# XML
cat demo_task_reports/xml/export_demo_tasks.xml

# Excel (avec LibreOffice)
libreoffice demo_task_reports/xlsx/export_demo_tasks.xlsx
```

## Note

Ces fichiers sont générés automatiquement et peuvent être supprimés et régénérés à tout moment en relançant les scripts de démonstration. 