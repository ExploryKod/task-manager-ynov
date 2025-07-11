# TaskManager YNOV

Projet final pour le cours de Méthodologie des Tests - Un gestionnaire de tâches robuste développé avec Python et une couverture de tests de 95%.

Mes réponses aux questions de départ sur Analyse et Conception : voir le fichier `AnalyseConception.md` (à la racine)
[cliquer ici](./AnalyseConception.md)

Mes réponses aux questions de la phase 10 sur la couverture de test : voir le fichier `AnalyseCoverage.md` (à la racine)
[cliquer ici](./AnalyseCoverage.md)

Mes rapports de couvertures de test sauvegardées: <br>

[Premier rapport avec couverture insuffisante](./rapports_couverture/premier/htmlcov/) <br>

Commande Make pour lire ce rapport : `make open-coverage-first`

Pour lire ce rapport dans votre navigateur aprés le clone du repo, aller là :<br> `<votre-chemin-de-fichier>/task-manager-ynov/rapports_couvertures/premier/htmlcov/index.html`<br><br>
Exemple sur une machine Linux : `file:///home/<votre-nom>/<chemin-depuis-dossier-utilisateur>/task-manager-ynov/rapports_couvertures/premier/htmlcov/index.html`

[Dernier rapport avec couverture 95%](./rapports_couverture/couverture_95percent/htmlcov/)

Commande Make pour lire ce rapport : `make open-coverage-final`

Pour lire ce rapport dans votre navigateur aprés le clone du repo, aller là :<br> `<votre-chemin-de-fichier>/task-manager-ynov/rapports_couvertures/couverture_95percent/htmlcov/index.html`<br><br>
Exemple sur une machine Linux : `file:///home/<votre-nom>/<chemin-depuis-dossier-utilisateur>/task-manager-ynov/rapports_couvertures/couverture_95percent/htmlcov/index.html`

Dernier test de couverture effectué : 

<img src="./last_couverture_test.png" alt="dernière couverture">

## 📋 Description

TaskManager est un système de gestion de tâches complet qui permet de :
- Créer, modifier et supprimer des tâches
- Gérer les priorités (LOW, MEDIUM, HIGH, URGENT)
- Suivre les statuts (TODO, IN_PROGRESS, DONE, CANCELLED)
- Sauvegarder et charger les données depuis des fichiers JSON
- Générer des statistiques détaillées
- Envoyer des notifications par email
- Générer des rapports

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <your-repository-url>
cd task-manager-ynov
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

Sur Linux/macOS :
```bash
source venv/bin/activate
```

Sur Windows :
```bash
venv\Scripts\activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Vérifier l'installation**
```bash
python -m pytest tests/ -v
```

## 🎯 Lancement de la démonstration

Une fois l'installation terminée, vous pouvez lancer la démonstration interactive :

```bash
python demo.py
```

### Ce que fait la démonstration :

1. **Création du gestionnaire** - Initialise un TaskManager
2. **Ajout de tâches** - Crée 4 tâches avec différentes priorités
3. **Marquage terminé** - Marque 2 tâches comme terminées
4. **Affichage des statistiques** - Montre les statistiques complètes
5. **Sauvegarde** - Enregistre les données dans `demo_task_reports/json/demo_tasks.json`
6. **Rechargement** - Vérifie que les données sont correctement restaurées

### Exemple de sortie :
```
=== Démonstration TaskManager ===

1. Création du gestionnaire de tâches...
Gestionnaire créé avec stockage: demo_tasks.json

2. Ajout de plusieurs tâches avec différentes priorités...
Tâche URGENT ajoutée (ID: 1752230487.414)
[...]

✓ Vérification réussie: Les données ont été sauvegardées et rechargées correctement!
```

### 📤 Export multi-format

Le TaskManager supporte l'export vers plusieurs formats :

```bash
python demo_export_simple.py
# ou avec make
make demo-export
```

#### Utilisation programmatique :

```python
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority

# Créer un gestionnaire avec des tâches
manager = TaskManager("my_tasks.json")
manager.add_task("Tâche importante", "Description", Priority.HIGH)

# Export vers JSON avec statistiques
manager.export_tasks("rapport.json", "json", include_statistics=True)

# Export vers XML
manager.export_tasks("rapport.xml", "xml", include_statistics=True)

# Export vers Excel
manager.export_tasks("rapport.xlsx", "xlsx", include_statistics=True)

# Voir les formats supportés
formats = manager.get_export_formats()
print(formats)  # ['json', 'xml', 'xlsx', 'excel']
```

#### Formats de sortie :

- **JSON** : Structure complète avec métadonnées et statistiques → `demo_task_reports/json/`
- **XML** : Format standard avec validation et hiérarchie claire → `demo_task_reports/xml/`
- **Excel** : Deux onglets (Tasks + Statistics) avec formatage professionnel → `demo_task_reports/xlsx/`

#### Organisation des fichiers

Les rapports sont automatiquement organisés dans des dossiers dédiés :
```
demo_task_reports/
├── json/    # Fichiers JSON (.json)
├── xml/     # Fichiers XML (.xml)
└── xlsx/    # Fichiers Excel (.xlsx)
```

## 🧪 Tests

### Lancer tous les tests
```bash
python -m pytest tests/ -v
```

### Tests avec couverture
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Voir le rapport de couverture
```bash
# Ouvrir htmlcov/index.html dans un navigateur
firefox htmlcov/index.html
```

### Statistiques de tests
- **112 tests** au total
- **100% de réussite**
- **95%+ de couverture** de code

## 📁 Structure du projet

```
task-manager-ynov/
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── task.py          # Classe Task et énumérations
│       ├── manager.py       # Gestionnaire principal
│       └── services.py      # Services (Email, Rapports, Export)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Configuration des tests
│   ├── test_task.py         # Tests de la classe Task
│   ├── test_task_manager.py # Tests du gestionnaire
│   └── test_services.py     # Tests des services
├── demo_task_reports/       # Rapports générés (organisés par format)
│   ├── json/                # Exports JSON
│   ├── xml/                 # Exports XML
│   ├── xlsx/                # Exports Excel
│   └── README.md           # Documentation des rapports
├── demo.py                  # Script de démonstration original
├── demo_export.py           # Démonstration complète de l'export
├── demo_export_simple.py    # Exemple simple d'export
├── Makefile                 # Commandes automatisées
├── requirements.txt         # Dépendances (openpyxl, lxml)
├── pytest.ini             # Configuration pytest
└── README.md               # Ce fichier
```

## ⚙️ Fonctionnalités principales

### 📤 Export multi-format
- **JSON** : Export structuré avec métadonnées
- **XML** : Format standard avec validation
- **Excel** : Fichiers .xlsx avec onglets séparés (Tasks + Statistics)
- **Statistiques incluses** : Optionnel dans tous les formats
- **Historique des exports** : Suivi des opérations d'export

### Gestion des tâches
- Création avec titre, description et priorité
- Modification du statut (TODO → IN_PROGRESS → DONE)
- Suppression de tâches
- Recherche par ID, priorité ou statut

### Persistance des données
- Sauvegarde automatique au format JSON
- Chargement depuis fichier
- Gestion des erreurs de fichier
- Validation des données

### Statistiques
- Taux de completion
- Répartition par priorité
- Répartition par statut
- Métadonnées temporelles

### Services
- **EmailService** : Notifications par email
- **ReportService** : Génération de rapports
- **ExportService** : Export vers différents formats

## 🔧 Configuration

### Fichier de configuration pytest (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --tb=short
pythonpath = .
```

### Variables d'environnement
- `PYTHONPATH` : Configuré pour inclure le répertoire racine
- Tests configurés pour fonctionner avec la structure `src/`

## 📊 Couverture de tests

Le projet maintient une couverture de tests supérieure à 95% :
- **task.py** : 99%
- **services.py** : 94%
- **manager.py** : 95%+

## 🤝 Contribution

Pour contribuer au projet :
1. Forkez le repository
2. Créez une branche pour votre fonctionnalité
3. Ajoutez des tests pour vos modifications
4. Assurez-vous que la couverture reste > 95%
5. Soumettez une pull request

## 📄 License

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 🎓 Contexte académique

Projet développé dans le cadre du cours "Méthodologie des Tests" à YNOV, démontrant :
- Tests unitaires et d'intégration
- Couverture de code
- Intégration continue (GitHub Actions)
- Documentation technique
- Bonnes pratiques de développement
