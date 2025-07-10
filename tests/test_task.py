import pytest
from datetime import datetime
from src.task_manager.task import Task, Priority, Status


class TestTaskCreation:
    """Tests de création de tâches"""

    def test_create_task_minimal(self):
        """Test création tâche avec paramètres minimaux"""
        # TODO: Créez une tâche avec juste un titre
        # TODO: Vérifiez tous les attributs par défaut
        pass

    def test_create_task_complete(self):
        """Test création tâche avec tous les paramètres"""
        # TODO: Créez une tâche avec titre, description, priorité
        # TODO: Vérifiez tous les attributs
        pass

    def test_create_task_empty_title_raises_error(self):
        """Test titre vide lève une erreur"""
        # TODO: Utilisez pytest.raises pour tester l'exception
        pass

    def test_create_task_invalid_priority_raises_error(self):
        """Test priorité invalide lève une erreur"""
        # TODO: Testez avec un mauvais type de priorité
        pass


class TestTaskOperations:
    """Tests des opérations sur les tâches"""

    def setup_method(self):
        """Fixture : tâche de test"""
        # TODO: Créez self.task pour les tests
        pass

    def test_mark_completed_changes_status(self):
        """Test marquage comme terminée"""
        # TODO: Marquez la tâche comme terminée
        # TODO: Vérifiez le changement de statut
        # TODO: Vérifiez que completed_at est défini
        pass

    def test_update_priority_valid(self):
        """Test mise à jour priorité valide"""
        # TODO: Changez la priorité
        # TODO: Vérifiez le changement
        pass

    def test_assign_to_project(self):
        """Test assignation à un projet"""
        # TODO: Assignez à un projet
        # TODO: Vérifiez l'assignation
        pass


class TestTaskSerialization:
    """Tests de sérialisation JSON"""

    def setup_method(self):
        # TODO: Créez une tâche complexe avec tous les attributs
        pass

    def test_to_dict_contains_all_fields(self):
        """Test conversion en dictionnaire"""
        # TODO: Convertissez en dict
        # TODO: Vérifiez que tous les champs sont présents
        # TODO: Vérifiez que les types sont sérialisables (str pour Enum/datetime)
        pass

    def test_from_dict_recreates_task(self):
        """Test recréation depuis dictionnaire"""
        # TODO: Convertissez en dict puis recréez
        # TODO: Vérifiez que les deux tâches sont équivalentes
        pass
