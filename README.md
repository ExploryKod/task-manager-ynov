# TaskManager YNOV

Projet final pour le cours de Méthodologie des Tests - Un gestionnaire de tâches robuste développé avec Python et une couverture de tests de 95%.

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
5. **Sauvegarde** - Enregistre les données dans `demo_tasks.json`
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
│       └── services.py      # Services (Email, Rapports)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Configuration des tests
│   ├── test_task.py         # Tests de la classe Task
│   ├── test_task_manager.py # Tests du gestionnaire
│   └── test_services.py     # Tests des services
├── demo.py                  # Script de démonstration
├── requirements.txt         # Dépendances
├── pytest.ini             # Configuration pytest
└── README.md               # Ce fichier
```

## ⚙️ Fonctionnalités principales

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
