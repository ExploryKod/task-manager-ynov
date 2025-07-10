import pytest
from unittest.mock import patch, mock_open
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status


class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""

    def setup_method(self):
        """Fixture : gestionnaire de test"""
        # TODO: Créez self.manager avec un fichier temporaire
        pass

    def test_add_task_returns_id(self):
        """Test ajout tâche retourne un ID"""
        # TODO: Ajoutez une tâche
        # TODO: Vérifiez que l'ID est retourné
        # TODO: Vérifiez que la tâche est dans la liste
        pass

    def test_get_task_existing(self):
        """Test récupération tâche existante"""
        # TODO: Ajoutez une tâche
        # TODO: Récupérez-la par ID
        # TODO: Vérifiez les propriétés
        pass

    def test_get_task_nonexistent_returns_none(self):
        """Test récupération tâche inexistante"""
        # TODO: Cherchez une tâche avec un ID bidon
        # TODO: Vérifiez que None est retourné
        pass


class TestTaskManagerFiltering:
    """Tests de filtrage des tâches"""

    def setup_method(self):
        """Fixture : gestionnaire avec plusieurs tâches"""
        self.manager = TaskManager("test_tasks.json")
        # TODO: Ajoutez 3-4 tâches avec différents statuts/priorités
        pass

    def test_get_tasks_by_status(self):
        """Test filtrage par statut"""
        # TODO: Filtrez les tâches TODO
        # TODO: Vérifiez le nombre et les propriétés
        pass

    def test_get_tasks_by_priority(self):
        """Test filtrage par priorité"""
        # TODO: Filtrez les tâches HIGH priority
        # TODO: Vérifiez le résultat
        pass


class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""

    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        # TODO: Ajoutez quelques tâches de test
        pass

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        """Test sauvegarde réussie"""
        # TODO: Appelez save_to_file()
        # TODO: Vérifiez que le fichier est ouvert en écriture
        # TODO: Vérifiez que json.dump est appelé
        pass

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_from_file_success(self, mock_json_load, mock_file):
        """Test chargement réussi"""
        # TODO: Configurez mock_json_load pour retourner des données de test
        # TODO: Appelez load_from_file()
        # TODO: Vérifiez que les tâches sont chargées
        pass

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_from_nonexistent_file(self, mock_file):
        """Test chargement fichier inexistant"""
        # TODO: Appelez load_from_file()
        # TODO: Vérifiez que ça ne plante pas
        # TODO: Vérifiez que la liste reste vide
        pass
