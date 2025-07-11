import pytest
from unittest.mock import patch, mock_open, Mock
import json
import tempfile
import os
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit  
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

    @patch('builtins.open', new_callable=mock_open, read_data='{"tasks": "not_an_array"}')
    @patch('json.load')
    @patch('os.path.exists', return_value=True)
    def test_load_from_file_with_invalid_tasks_format_should_raise_error(self, mock_exists, mock_json_load, mock_file):
        """Test chargement avec format tâches invalide (pas un array)"""
        mock_json_load.return_value = {"tasks": "not_an_array"}
        
        with pytest.raises(RuntimeError, match="Unexpected error while loading tasks.*Invalid tasks format"):
            self.manager.load_from_file("invalid.json")


@pytest.mark.unit
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


@pytest.mark.unit
class TestTaskManagerPersistenceAdvanced:
    """Tests avancés de persistence pour améliorer la couverture"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path

    def teardown_method(self):
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    # @patch('builtins.open', new_callable=mock_open, read_data='{"invalid": "structure"}')
    # @patch('json.load')
    # def test_load_from_file_with_invalid_json_structure(self, mock_json_load, mock_file):
    #     """Test chargement avec structure JSON invalide (pas un dict)"""
    #     mock_json_load.return_value = ["not", "a", "dict"]
        
    #     with pytest.raises(ValueError, match="Invalid JSON structure.*expected object"):
    #         self.manager.load_from_file("invalid.json")

    # @patch('builtins.open', new_callable=mock_open, read_data='{"tasks": "not_an_array"}')
    # @patch('json.load')
    # def test_load_from_file_with_invalid_tasks_format(self, mock_json_load, mock_file):
    #     """Test chargement avec format tâches invalide (pas un array)"""
    #     mock_json_load.return_value = {"tasks": "not_an_array"}
        
    #     with pytest.raises(ValueError, match="Invalid tasks format.*expected array"):
    #         self.manager.load_from_file("invalid.json")

    # @patch('builtins.open', new_callable=mock_open)
    # @patch('json.load')
    # def test_load_from_file_with_malformed_task_data(self, mock_json_load, mock_file):
    #     """Test chargement avec données de tâche malformées"""
    #     mock_json_load.return_value = {
    #         "tasks": [{"incomplete": "task_data"}]  # Manque les champs requis
    #     }
        
    #     with pytest.raises(ValueError, match="Invalid task data at index 0"):
    #         self.manager.load_from_file("malformed.json")

    # @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    # def test_load_from_file_permission_denied(self, mock_file):
    #     """Test chargement avec permission refusée"""
    #     with pytest.raises(PermissionError, match="Cannot read file.*Permission denied"):
    #         self.manager.load_from_file("no_permission.json")

    @patch('builtins.open', side_effect=OSError("I/O error"))
    def test_save_to_file_os_error(self, mock_file):
        """Test sauvegarde avec erreur système"""
        with pytest.raises(OSError, match="File system error while saving"):
            self.manager.save_to_file("error.json")

    @patch('builtins.open', side_effect=RuntimeError("Unexpected error"))
    def test_save_to_file_unexpected_error(self, mock_file):
        """Test sauvegarde avec erreur inattendue"""
        with pytest.raises(RuntimeError, match="Unexpected error while saving"):
            self.manager.save_to_file("error.json")


@pytest.mark.unit
class TestTaskManagerUtilityMethods:
    """Tests des méthodes utilitaires pour améliorer la couverture"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path

    def teardown_method(self):
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    def test_get_all_tasks_returns_copy(self):
        """Test que get_all_tasks retourne une copie, pas la référence"""
        task_id = self.manager.add_task("Test task")
        
        tasks_copy = self.manager.get_all_tasks()
        tasks_copy.clear()  # Modifier la copie
        
        # La liste originale ne doit pas être affectée
        assert len(self.manager.get_all_tasks()) == 1

    def test_clear_all_tasks_empties_manager(self):
        """Test que clear_all_tasks vide complètement le gestionnaire"""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        
        assert len(self.manager.get_all_tasks()) == 3
        
        self.manager.clear_all_tasks()
        
        assert len(self.manager.get_all_tasks()) == 0
        assert self.manager.get_task_count() == 0

    def test_get_task_count_accuracy(self):
        """Test précision du compteur de tâches"""
        assert self.manager.get_task_count() == 0
        
        self.manager.add_task("Task 1")
        assert self.manager.get_task_count() == 1
        
        task_id = self.manager.add_task("Task 2")
        assert self.manager.get_task_count() == 2
        
        self.manager.delete_task(task_id)
        assert self.manager.get_task_count() == 1

    def test_len_magic_method(self):
        """Test méthode magique __len__"""
        assert len(self.manager) == 0
        
        self.manager.add_task("Task")
        assert len(self.manager) == 1
        
        # Vérifier cohérence avec get_task_count
        assert len(self.manager) == self.manager.get_task_count()

    def test_iter_magic_method(self):
        """Test méthode magique __iter__"""
        task_id1 = self.manager.add_task("Task 1")
        task_id2 = self.manager.add_task("Task 2")
        
        # Tester l'itération
        task_ids_found = []
        for task in self.manager:
            task_ids_found.append(task.id)
        
        assert task_id1 in task_ids_found
        assert task_id2 in task_ids_found
        assert len(task_ids_found) == 2

    def test_repr_magic_method(self):
        """Test méthode magique __repr__"""
        repr_str = repr(self.manager)
        
        assert "TaskManager" in repr_str
        assert "tasks=0" in repr_str
        assert self.temp_path in repr_str
        
        self.manager.add_task("Test")
        repr_str = repr(self.manager)
        assert "tasks=1" in repr_str

    def test_get_current_time_iso_format(self):
        """Test format ISO du timestamp"""
        # Accéder à la méthode privée pour test
        timestamp = self.manager._get_current_time_iso()
        
        # Vérifier format ISO (doit contenir 'T' et être parseable)
        assert 'T' in timestamp
        
        # Vérifier que c'est un timestamp valide
        from datetime import datetime
        parsed_time = datetime.fromisoformat(timestamp)
        assert isinstance(parsed_time, datetime)


@pytest.mark.unit
class TestTaskManagerEdgeCases:
    """Tests des cas limites et validations d'erreur"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path

    def teardown_method(self):
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    def test_delete_task_with_invalid_id_types(self):
        """Test suppression avec types d'ID invalides"""
        # Test avec chaîne non convertible
        assert self.manager.delete_task("invalid_string") == False
        
        # Test avec type complexe
        assert self.manager.delete_task({"invalid": "dict"}) == False
        
        # Test avec liste
        assert self.manager.delete_task([1, 2, 3]) == False

    @patch('os.makedirs', side_effect=OSError("Cannot create directory"))
    def test_validate_storage_environment_creation_error(self, mock_makedirs):
        """Test création d'environnement avec erreur"""
        # Créer un gestionnaire avec un chemin qui n'existe pas
        fake_path = "/fake/path/that/does/not/exist/tasks.json"
        
        with pytest.raises(OSError, match="Cannot create storage directory"):
            manager = TaskManager(fake_path)
            manager._validate_storage_environment()

    @patch('os.listdir', side_effect=OSError("Permission denied"))
    def test_validate_json_file_limits_os_error_ignored(self, mock_listdir):
        """Test validation limites avec erreur OS ignorée"""
        # Cette méthode doit passer silencieusement même avec OSError
        try:
            self.manager._validate_json_file_limits()
            # Si on arrive ici, c'est bon (l'exception OSError est ignorée)
        except OSError:
            pytest.fail("OSError should be silently ignored in _validate_json_file_limits")


@pytest.mark.unit
class TestTaskManagerStorageValidation:
    """Tests de validation du stockage"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path

    def teardown_method(self):
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_validate_storage_environment_creates_directory(self, mock_makedirs, mock_exists):
        """Test création de répertoire pour stockage"""
        self.manager._validate_storage_environment()
        
        # Vérifier que makedirs a été appelé
        mock_makedirs.assert_called_once()

    @patch('os.listdir')
    def test_validate_json_file_limits_within_limit(self, mock_listdir):
        """Test validation avec nombre de fichiers dans la limite"""
        # Simuler 50 fichiers JSON (bien en dessous de la limite de 150)
        mock_listdir.return_value = [f"file_{i}.json" for i in range(50)]
        
        # Ne doit pas lever d'exception
        try:
            self.manager._validate_json_file_limits()
        except ValueError:
            pytest.fail("Should not raise ValueError when within file limits")

    @patch('os.listdir')
    def test_validate_json_file_limits_mixed_files(self, mock_listdir):
        """Test validation avec mélange de fichiers"""
        # Mélanger fichiers JSON et non-JSON
        mock_listdir.return_value = [
            "file1.json", "file2.txt", "file3.json", 
            "document.pdf", "file4.json"
        ]
        
        # Ne doit pas lever d'exception (seulement 3 fichiers JSON)
        try:
            self.manager._validate_json_file_limits()
        except ValueError:
            pytest.fail("Should only count .json files for limit validation")


@pytest.mark.unit
class TestTaskManagerExport:
    """Tests des fonctionnalités d'export du TaskManager"""

    def setup_method(self):
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.manager = TaskManager(temp_path)
        self.temp_path = temp_path
        
        # Ajouter quelques tâches de test
        self.manager.add_task("Task 1", "Description 1", Priority.HIGH)
        self.manager.add_task("Task 2", "Description 2", Priority.MEDIUM)

    def teardown_method(self):
        try:
            os.unlink(self.temp_path)
        except OSError:
            pass

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_should_delegate_to_export_service(self, mock_export):
        """Test que export_tasks délègue au service d'export"""
        mock_export.return_value = True
        
        result = self.manager.export_tasks("test.json", "json", True)
        
        assert result is True
        mock_export.assert_called_once()
        args, kwargs = mock_export.call_args
        assert args[0] == self.manager._tasks  # Liste des tâches
        assert args[1] == "test.json"          # Nom du fichier
        assert args[2] == "json"               # Format
        assert args[3] is True                 # Include statistics

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_with_default_parameters(self, mock_export):
        """Test export_tasks avec paramètres par défaut"""
        mock_export.return_value = True
        
        result = self.manager.export_tasks("test_default.json")
        
        assert result is True
        args, kwargs = mock_export.call_args
        assert args[2] == "json"  # Format par défaut
        assert args[3] is True    # Include statistics par défaut

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_should_pass_current_tasks(self, mock_export):
        """Test que export_tasks passe les tâches actuelles"""
        mock_export.return_value = True
        
        # Ajouter une tâche supplémentaire
        self.manager.add_task("Additional Task")
        
        self.manager.export_tasks("test_current.json")
        
        args, kwargs = mock_export.call_args
        tasks_passed = args[0]
        assert len(tasks_passed) == 3  # 2 tâches initiales + 1 ajoutée

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_should_handle_export_service_errors(self, mock_export):
        """Test gestion des erreurs du service d'export"""
        mock_export.side_effect = ValueError("Export error")
        
        with pytest.raises(ValueError, match="Export error"):
            self.manager.export_tasks("test_error.json")

    @patch('src.task_manager.services.ExportService.get_supported_formats')
    def test_get_export_formats_should_delegate_to_export_service(self, mock_get_formats):
        """Test que get_export_formats délègue au service d'export"""
        expected_formats = ['json', 'xml', 'xlsx', 'excel']
        mock_get_formats.return_value = expected_formats
        
        result = self.manager.get_export_formats()
        
        assert result == expected_formats
        mock_get_formats.assert_called_once()

    @patch('src.task_manager.services.ExportService')
    def test_export_tasks_creates_new_export_service_instance(self, mock_export_service_class):
        """Test que export_tasks crée une nouvelle instance d'ExportService"""
        mock_service_instance = Mock()
        mock_service_instance.export_tasks.return_value = True
        mock_export_service_class.return_value = mock_service_instance
        
        self.manager.export_tasks("test_instance.json")
        
        # Vérifier qu'une nouvelle instance est créée
        mock_export_service_class.assert_called_once()
        # Vérifier que la méthode export_tasks est appelée sur l'instance
        mock_service_instance.export_tasks.assert_called_once()

    @patch('src.task_manager.services.ExportService')
    def test_get_export_formats_creates_new_export_service_instance(self, mock_export_service_class):
        """Test que get_export_formats crée une nouvelle instance d'ExportService"""
        mock_service_instance = Mock()
        mock_service_instance.get_supported_formats.return_value = ['json', 'xml']
        mock_export_service_class.return_value = mock_service_instance
        
        self.manager.get_export_formats()
        
        # Vérifier qu'une nouvelle instance est créée
        mock_export_service_class.assert_called_once()
        # Vérifier que la méthode get_supported_formats est appelée sur l'instance
        mock_service_instance.get_supported_formats.assert_called_once()

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_with_different_formats(self, mock_export):
        """Test export_tasks avec différents formats"""
        mock_export.return_value = True
        formats_to_test = ["json", "xml", "xlsx", "excel"]
        
        for fmt in formats_to_test:
            self.manager.export_tasks(f"test.{fmt}", fmt)
            
            # Vérifier que le format correct est passé
            args, kwargs = mock_export.call_args
            assert args[2] == fmt

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_with_statistics_flag(self, mock_export):
        """Test export_tasks avec flag statistiques"""
        mock_export.return_value = True
        
        # Test avec statistiques
        self.manager.export_tasks("test_with_stats.json", include_statistics=True)
        args, kwargs = mock_export.call_args
        assert args[3] is True
        
        # Test sans statistiques
        self.manager.export_tasks("test_without_stats.json", include_statistics=False)
        args, kwargs = mock_export.call_args
        assert args[3] is False

    @patch('src.task_manager.services.ExportService.export_tasks')
    def test_export_tasks_return_value_propagation(self, mock_export):
        """Test que export_tasks propage la valeur de retour du service"""
        # Test avec succès
        mock_export.return_value = True
        result = self.manager.export_tasks("test_success.json")
        assert result is True
        
        # Test avec échec
        mock_export.return_value = False
        result = self.manager.export_tasks("test_failure.json")
        assert result is False


@pytest.mark.integration
class TestTaskManagerRealFileOperations:
    """Tests d'intégration - opérations réelles sur fichiers"""
    
    def setup_method(self):
        """Fixture : fichier temporaire réel"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, 'test_tasks.json')
        self.manager = TaskManager(self.temp_file)
    
    def teardown_method(self):
        """Nettoyage fichiers temporaires"""
        # Supprimer tous les fichiers du répertoire temporaire
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        # Supprimer le répertoire
        os.rmdir(self.temp_dir)
    
    def test_full_save_and_load_cycle_should_preserve_all_data(self):
        """Test intégration complet : sauvegarde et rechargement"""
        # Ajouter des tâches avec différentes priorités et statuts
        task1_id = self.manager.add_task("Tâche urgente", "Description urgente", Priority.URGENT)
        task2_id = self.manager.add_task("Tâche normale", "Description normale", Priority.MEDIUM)
        task3_id = self.manager.add_task("Tâche basse", "Description basse", Priority.LOW)
        
        # Marquer une tâche comme terminée
        task1 = self.manager.get_task(task1_id)
        task1.mark_completed()
        
        # Sauvegarder
        self.manager.save_to_file(self.temp_file)
        
        # Créer nouveau gestionnaire et charger
        new_manager = TaskManager(self.temp_file)
        new_manager.load_from_file(self.temp_file)
        
        # Vérifier que toutes les données sont préservées
        assert len(new_manager.get_all_tasks()) == 3
        
        loaded_task1 = new_manager.get_task(task1_id)
        loaded_task2 = new_manager.get_task(task2_id)
        loaded_task3 = new_manager.get_task(task3_id)
        
        assert loaded_task1.title == "Tâche urgente"
        assert loaded_task1.priority == Priority.URGENT
        assert loaded_task1.status == Status.DONE
        
        assert loaded_task2.title == "Tâche normale"
        assert loaded_task2.priority == Priority.MEDIUM
        assert loaded_task2.status == Status.TODO
        
        assert loaded_task3.title == "Tâche basse"
        assert loaded_task3.priority == Priority.LOW
        assert loaded_task3.status == Status.TODO
    
    def test_export_and_verify_real_json_file(self):
        """Test intégration : export JSON réel"""
        # Créer des tâches
        self.manager.add_task("Export test 1", "Description 1", Priority.HIGH)
        self.manager.add_task("Export test 2", "Description 2", Priority.LOW)
        
        # Export vers fichier réel
        export_file = os.path.join(self.temp_dir, 'export_test.json')
        result = self.manager.export_tasks(export_file, 'json', include_statistics=True)
        
        assert result is True
        assert os.path.exists(export_file)
        
        # Vérifier le contenu du fichier
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert 'tasks' in data
        assert 'statistics' in data
        assert len(data['tasks']) == 2
        assert data['statistics']['total_tasks'] == 2
        assert data['statistics']['completion_rate'] == 0.0
    
    def test_concurrent_manager_access_same_file(self):
        """Test intégration : accès concurrent au même fichier"""
        # Premier gestionnaire ajoute des tâches
        task1_id = self.manager.add_task("Tâche 1", "Description 1", Priority.HIGH)
        self.manager.save_to_file(self.temp_file)
        
        # Deuxième gestionnaire charge et ajoute des tâches
        manager2 = TaskManager(self.temp_file)
        manager2.load_from_file(self.temp_file)
        task2_id = manager2.add_task("Tâche 2", "Description 2", Priority.LOW)
        
        # Vérifier que les deux gestionnaires ont accès aux bonnes données
        assert len(self.manager.get_all_tasks()) == 1
        assert len(manager2.get_all_tasks()) == 2
        
        # Sauvegarder le second gestionnaire
        manager2.save_to_file(self.temp_file)
        
        # Recharger le premier gestionnaire
        self.manager.load_from_file(self.temp_file)
        assert len(self.manager.get_all_tasks()) == 2


@pytest.mark.integration
class TestTaskManagerWorkflows:
    """Tests d'intégration - workflows complets"""
    
    def setup_method(self):
        """Fixture : environnement de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = TaskManager(os.path.join(self.temp_dir, 'workflow_test.json'))
    
    def teardown_method(self):
        """Nettoyage"""
        for file in os.listdir(self.temp_dir):
            os.unlink(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_complete_project_workflow(self):
        """Test workflow complet d'un projet"""
        # 1. Créer un projet avec plusieurs tâches
        project_tasks = [
            ("Analyse des besoins", "Définir les fonctionnalités", Priority.HIGH),
            ("Développement", "Coder l'application", Priority.MEDIUM),
            ("Tests", "Tester l'application", Priority.MEDIUM),
            ("Déploiement", "Mettre en production", Priority.LOW)
        ]
        
        task_ids = []
        for title, desc, priority in project_tasks:
            task_id = self.manager.add_task(title, desc, priority)
            task_ids.append(task_id)
        
        # 2. Simuler l'avancement du projet
        # Terminer l'analyse
        self.manager.get_task(task_ids[0]).mark_completed()
        
        # Vérifier les statistiques à mi-parcours
        stats = self.manager.get_statistics()
        assert stats['total_tasks'] == 4
        assert stats['completed_tasks'] == 1
        assert stats['completion_rate'] == 25.0
        
        # 3. Continuer le projet
        self.manager.get_task(task_ids[1]).mark_completed()
        self.manager.get_task(task_ids[2]).mark_completed()
        
        # 4. Export du rapport d'avancement
        json_file = os.path.join(self.temp_dir, 'project_report.json')
        xml_file = os.path.join(self.temp_dir, 'project_report.xml')
        
        self.manager.export_tasks(json_file, 'json', include_statistics=True)
        self.manager.export_tasks(xml_file, 'xml', include_statistics=True)
        
        # Vérifier que les fichiers sont créés
        assert os.path.exists(json_file)
        assert os.path.exists(xml_file)
        
        # 5. Finaliser le projet
        self.manager.get_task(task_ids[3]).mark_completed()
        
        # Vérifier la completion finale
        final_stats = self.manager.get_statistics()
        assert final_stats['completion_rate'] == 100.0
        assert final_stats['status_distribution']['done'] == 4
        assert final_stats['status_distribution']['todo'] == 0
    
    def test_multi_format_export_integration(self):
        """Test intégration : export vers plusieurs formats"""
        # Créer un dataset de test complet
        priorities = [Priority.URGENT, Priority.HIGH, Priority.MEDIUM, Priority.LOW]
        for i, priority in enumerate(priorities):
            task_id = self.manager.add_task(f"Task {i+1}", f"Description {i+1}", priority)
            if i < 2:  # Marquer les 2 premières comme terminées
                self.manager.get_task(task_id).mark_completed()
        
        # Export vers tous les formats supportés
        formats = self.manager.get_export_formats()
        export_files = {}
        
        for fmt in formats:
            if fmt == 'excel':
                continue  # Skip excel alias
            filename = os.path.join(self.temp_dir, f'export_test.{fmt}')
            result = self.manager.export_tasks(filename, fmt, include_statistics=True)
            assert result is True
            assert os.path.exists(filename)
            export_files[fmt] = filename
        
        # Vérifier que tous les formats ont été créés
        assert 'json' in export_files
        assert 'xml' in export_files
        assert 'xlsx' in export_files
        
        # Vérifier la taille des fichiers (doivent contenir des données)
        for fmt, filepath in export_files.items():
            assert os.path.getsize(filepath) > 0
