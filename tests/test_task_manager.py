import pytest
from unittest.mock import patch, mock_open
import json
import tempfile
import os
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status


class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""

    def setup_method(self):
        """Fixture : gestionnaire de test"""
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path

    def teardown_method(self):
        """Nettoyage fichiers temporaires"""
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    def test_add_task_with_title_only_should_return_float_id(self):
        """Test ajout tâche retourne un ID"""
        task_id = self.manager.add_task("Nouvelle tâche")
        
        assert isinstance(task_id, float)
        assert task_id > 0

    def test_add_task_should_store_task_in_manager(self):
        """Test ajout tâche stocke dans gestionnaire"""
        task_id = self.manager.add_task("Tâche test")
        
        assert len(self.manager.get_all_tasks()) == 1
        stored_task = self.manager.get_task(task_id)
        assert stored_task.title == "Tâche test"

    def test_add_task_with_all_parameters_should_set_attributes(self):
        """Test ajout tâche avec tous paramètres"""
        task_id = self.manager.add_task(
            "Tâche complète", 
            "Description détaillée", 
            Priority.HIGH
        )
        
        task = self.manager.get_task(task_id)
        assert task.title == "Tâche complète"
        assert task.description == "Description détaillée"
        assert task.priority == Priority.HIGH

    def test_get_task_with_existing_id_should_return_task(self):
        """Test récupération tâche existante"""
        task_id = self.manager.add_task("Tâche existante")
        
        retrieved_task = self.manager.get_task(task_id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Tâche existante"

    def test_get_task_with_nonexistent_id_should_return_none(self):
        """Test récupération tâche inexistante"""
        result = self.manager.get_task(999999.999)
        
        assert result is None

    def test_get_task_with_none_id_should_return_none(self):
        """Test récupération avec ID None"""
        result = self.manager.get_task(None)
        
        assert result is None

    def test_get_task_with_invalid_id_type_should_return_none(self):
        """Test récupération avec ID type invalide"""
        result = self.manager.get_task("invalid_id")
        
        assert result is None

    def test_delete_task_with_existing_id_should_return_true(self):
        """Test suppression tâche existante"""
        task_id = self.manager.add_task("Tâche à supprimer")
        
        result = self.manager.delete_task(task_id)
        
        assert result is True
        assert self.manager.get_task(task_id) is None

    def test_delete_task_with_nonexistent_id_should_return_false(self):
        """Test suppression tâche inexistante"""
        result = self.manager.delete_task(999999.999)
        
        assert result is False

    def test_delete_task_with_none_id_should_return_false(self):
        """Test suppression avec ID None"""
        result = self.manager.delete_task(None)
        
        assert result is False


class TestTaskManagerFiltering:
    """Tests de filtrage des tâches"""

    def setup_method(self):
        """Fixture : gestionnaire avec plusieurs tâches"""
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path
        
        self.todo_id = self.manager.add_task("Tâche TODO", priority=Priority.LOW)
        self.urgent_id = self.manager.add_task("Tâche urgente", priority=Priority.URGENT)
        self.high_id = self.manager.add_task("Tâche importante", priority=Priority.HIGH)
        
        todo_task = self.manager.get_task(self.todo_id)
        urgent_task = self.manager.get_task(self.urgent_id)
        urgent_task.mark_completed()

    def teardown_method(self):
        """Nettoyage fichiers temporaires"""
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    def test_get_tasks_by_status_todo_should_return_pending_tasks(self):
        """Test filtrage par statut TODO"""
        todo_tasks = self.manager.get_tasks_by_status(Status.TODO)
        
        assert len(todo_tasks) == 2
        assert all(task.status == Status.TODO for task in todo_tasks)

    def test_get_tasks_by_status_done_should_return_completed_tasks(self):
        """Test filtrage par statut DONE"""
        done_tasks = self.manager.get_tasks_by_status(Status.DONE)
        
        assert len(done_tasks) == 1
        assert done_tasks[0].status == Status.DONE

    def test_get_tasks_by_status_with_invalid_type_should_raise_error(self):
        """Test filtrage statut type invalide lève erreur"""
        with pytest.raises(TypeError, match="Status must be a Status enum"):
            self.manager.get_tasks_by_status("invalid")

    def test_get_tasks_by_priority_high_should_return_high_priority_tasks(self):
        """Test filtrage par priorité HIGH"""
        high_tasks = self.manager.get_tasks_by_priority(Priority.HIGH)
        
        assert len(high_tasks) == 1
        assert high_tasks[0].priority == Priority.HIGH

    def test_get_tasks_by_priority_urgent_should_return_urgent_tasks(self):
        """Test filtrage par priorité URGENT"""
        urgent_tasks = self.manager.get_tasks_by_priority(Priority.URGENT)
        
        assert len(urgent_tasks) == 1
        assert urgent_tasks[0].priority == Priority.URGENT

    def test_get_tasks_by_priority_with_invalid_type_should_raise_error(self):
        """Test filtrage priorité type invalide lève erreur"""
        with pytest.raises(TypeError, match="Priority must be a Priority enum"):
            self.manager.get_tasks_by_priority("high")


class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path
        
        self.manager.add_task("Tâche test 1", "Description 1", Priority.HIGH)
        self.manager.add_task("Tâche test 2", "Description 2", Priority.LOW)

    def teardown_method(self):
        """Nettoyage fichiers temporaires"""
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_should_open_file_for_writing(self, mock_json_dump, mock_file):
        """Test sauvegarde ouvre fichier en écriture"""
        self.manager.save_to_file("test.json")
        
        mock_file.assert_called_once_with("test.json", 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_should_call_json_dump(self, mock_json_dump, mock_file):
        """Test sauvegarde appelle json.dump"""
        self.manager.save_to_file("test.json")
        
        mock_json_dump.assert_called_once()
        call_args = mock_json_dump.call_args[0]
        data = call_args[0]
        assert "tasks" in data
        assert "metadata" in data

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_save_to_file_permission_denied_should_raise_specific_error(self, mock_file):
        """Test sauvegarde permission refusée lève erreur"""
        with pytest.raises(PermissionError, match="Cannot write to file.*Permission denied"):
            self.manager.save_to_file("readonly.json")

    # @patch('builtins.open', new_callable=mock_open, read_data='{"tasks": [], "metadata": {}}')
    # @patch('json.load')
    # def test_load_from_file_should_call_json_load(self, mock_json_load, mock_file):
    #     """Test chargement appelle json.load"""
    #     mock_json_load.return_value = {"tasks": [], "metadata": {}}
        
    #     self.manager.load_from_file("test.json")
        
    #     mock_json_load.assert_called_once()

    # @patch('builtins.open', new_callable=mock_open, read_data='{"tasks": []}')
    # @patch('json.load')
    # def test_load_from_file_with_valid_data_should_load_tasks(self, mock_json_load, mock_file):
    #     """Test chargement données valides charge tâches"""
    #     task_data = {
    #         "tasks": [{
    #             "id": 123456.789,
    #             "title": "Tâche chargée",
    #             "description": "Description",
    #             "priority": "medium",
    #             "status": "todo",
    #             "created_at": "2024-01-01T00:00:00.000000",
    #             "completed_at": None,
    #             "project_id": None
    #         }]
    #     }
    #     mock_json_load.return_value = task_data
        
    #     self.manager.load_from_file("test.json")
        
    #     assert len(self.manager.get_all_tasks()) == 1
    #     loaded_task = self.manager.get_all_tasks()[0]
    #     assert loaded_task.title == "Tâche chargée"

    @patch('os.path.exists', return_value=False)
    def test_load_from_nonexistent_file_should_not_crash(self, mock_exists):
        """Test chargement fichier inexistant ne plante pas"""
        initial_count = len(self.manager.get_all_tasks())
        
        self.manager.load_from_file("nonexistent.json")
        
        assert len(self.manager.get_all_tasks()) == 0

    # @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    # @patch('json.load', side_effect=json.JSONDecodeError("Invalid JSON", "doc", 0))
    # def test_load_from_corrupted_file_should_raise_json_error(self, mock_json_load, mock_file):
    #     """Test chargement fichier corrompu lève erreur JSON"""
    #     with pytest.raises(json.JSONDecodeError, match="Invalid JSON format"):
    #         self.manager.load_from_file("corrupted.json")

    @patch('os.listdir')
    def test_save_with_too_many_json_files_should_raise_error(self, mock_listdir):
        """Test sauvegarde dépassement limite fichiers JSON"""
        mock_listdir.return_value = [f"file_{i}.json" for i in range(151)]
        
        with pytest.raises(ValueError, match="Maximum number of JSON files exceeded"):
            self.manager.save_to_file("new_file.json")


class TestTaskManagerStatistics:
    """Tests de génération de statistiques"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path

    def teardown_method(self):
        """Nettoyage fichiers temporaires"""
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    def test_get_statistics_with_empty_manager_should_return_zero_values(self):
        """Test statistiques gestionnaire vide"""
        stats = self.manager.get_statistics()
        
        assert stats["total_tasks"] == 0
        assert stats["completed_tasks"] == 0
        assert stats["completion_rate"] == 0.0
        assert "No tasks found" in stats["message"]

    def test_get_statistics_with_all_pending_tasks_should_return_zero_completion(self):
        """Test statistiques toutes tâches en attente"""
        self.manager.add_task("Tâche 1")
        self.manager.add_task("Tâche 2")
        
        stats = self.manager.get_statistics()
        
        assert stats["total_tasks"] == 2
        assert stats["completed_tasks"] == 0
        assert stats["completion_rate"] == 0.0

    def test_get_statistics_with_all_completed_tasks_should_return_hundred_percent(self):
        """Test statistiques toutes tâches terminées"""
        task_id1 = self.manager.add_task("Tâche 1")
        task_id2 = self.manager.add_task("Tâche 2")
        
        self.manager.get_task(task_id1).mark_completed()
        self.manager.get_task(task_id2).mark_completed()
        
        stats = self.manager.get_statistics()
        
        assert stats["total_tasks"] == 2
        assert stats["completed_tasks"] == 2
        assert stats["completion_rate"] == 100.0

    def test_get_statistics_should_include_priority_distribution(self):
        """Test statistiques inclut distribution priorités"""
        self.manager.add_task("Tâche LOW", priority=Priority.LOW)
        self.manager.add_task("Tâche HIGH", priority=Priority.HIGH)
        self.manager.add_task("Tâche HIGH 2", priority=Priority.HIGH)
        
        stats = self.manager.get_statistics()
        
        assert stats["priority_distribution"]["low"] == 1
        assert stats["priority_distribution"]["high"] == 2
        assert stats["priority_distribution"]["medium"] == 0
        assert stats["priority_distribution"]["urgent"] == 0

    def test_get_statistics_should_include_status_distribution(self):
        """Test statistiques inclut distribution statuts"""
        task_id1 = self.manager.add_task("Tâche TODO")
        task_id2 = self.manager.add_task("Tâche DONE")
        self.manager.get_task(task_id2).mark_completed()
        
        stats = self.manager.get_statistics()
        
        assert stats["status_distribution"]["todo"] == 1
        assert stats["status_distribution"]["done"] == 1
        assert stats["status_distribution"]["in_progress"] == 0
        assert stats["status_distribution"]["cancelled"] == 0

    @pytest.mark.parametrize("total,completed,expected_rate", [
        (1, 0, 0.0),
        (1, 1, 100.0),
        (4, 1, 25.0),
        (4, 2, 50.0),
        (4, 3, 75.0),
        (3, 3, 100.0),
    ])
    def test_get_statistics_completion_rate_calculation(self, total, completed, expected_rate):
        """Test calcul taux completion diverses combinaisons"""
        task_ids = []
        for i in range(total):
            task_id = self.manager.add_task(f"Tâche {i+1}")
            task_ids.append(task_id)
        
        for i in range(completed):
            self.manager.get_task(task_ids[i]).mark_completed()
        
        stats = self.manager.get_statistics()
        
        assert stats["completion_rate"] == expected_rate
