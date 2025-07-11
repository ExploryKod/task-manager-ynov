import pytest
from datetime import datetime
from src.task_manager.task import Task, Priority, Status


class TestTaskCreation:
    """Tests de création de tâches"""

    def test_create_task_with_title_only_should_use_defaults(self):
        """Test création tâche avec paramètres minimaux"""
        task = Task("Tâche de test")
        
        assert task.title == "Tâche de test"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert task.status == Status.TODO
        assert isinstance(task.id, float)
        assert isinstance(task.created_at, datetime)
        assert task.completed_at is None
        assert task.project_id is None

    def test_create_task_with_all_parameters_should_set_all_attributes(self):
        """Test création tâche avec tous les paramètres"""
        task = Task(
            title="Tâche complète",
            description="Description détaillée",
            priority=Priority.HIGH
        )
        
        assert task.title == "Tâche complète"
        assert task.description == "Description détaillée"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO
        assert isinstance(task.id, float)
        assert isinstance(task.created_at, datetime)

    def test_create_task_with_empty_title_should_raise_error(self):
        """Test titre vide lève une erreur"""
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace only"):
            Task("")

    def test_create_task_with_whitespace_title_should_raise_error(self):
        """Test titre espaces lève une erreur"""
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace only"):
            Task("   ")

    def test_create_task_with_none_title_should_raise_error(self):
        """Test titre None lève une erreur"""
        with pytest.raises(TypeError, match="Title must be a string"):
            Task(None)

    def test_create_task_with_invalid_priority_type_should_raise_error(self):
        """Test priorité invalide lève une erreur"""
        with pytest.raises(TypeError, match="Priority must be a Priority enum"):
            Task("Test", priority="invalid")

    @pytest.mark.parametrize("title_length,should_pass", [
        (1, True),      # Minimum valide
        (100, True),    # Maximum valide
        (101, False),   # Dépassement
    ])
    def test_create_task_title_length_boundaries(self, title_length, should_pass):
        """Test limites longueur titre"""
        title = "A" * title_length
        
        if should_pass:
            task = Task(title)
            assert len(task.title) == title_length
        else:
            with pytest.raises(ValueError, match="Title cannot exceed 100 characters"):
                Task(title)

    def test_create_task_with_html_characters_should_raise_error(self):
        """Test titre avec HTML lève une erreur"""
        with pytest.raises(ValueError, match="Title contains invalid characters"):
            Task("<script>alert('xss')</script>")

    def test_create_task_strips_whitespace_from_title_and_description(self):
        """Test nettoyage espaces titre et description"""
        task = Task("  Titre avec espaces  ", "  Description avec espaces  ")
        
        assert task.title == "Titre avec espaces"
        assert task.description == "Description avec espaces"


class TestTaskOperations:
    """Tests des opérations sur les tâches"""

    def setup_method(self):
        """Fixture : tâche de test"""
        self.task = Task("Tâche de test", "Description de test", Priority.MEDIUM)

    def test_mark_completed_should_change_status_to_done(self):
        """Test marquage comme terminée"""
        self.task.mark_completed()
        
        assert self.task.status == Status.DONE

    def test_mark_completed_should_set_completed_at_timestamp(self):
        """Test marquage terminée définit timestamp"""
        before_completion = datetime.now()
        self.task.mark_completed()
        after_completion = datetime.now()
        
        assert self.task.completed_at is not None
        assert before_completion <= self.task.completed_at <= after_completion

    def test_mark_completed_on_already_completed_task_should_raise_error(self):
        """Test marquage terminée sur tâche déjà terminée lève erreur"""
        self.task.mark_completed()
        
        with pytest.raises(ValueError, match="Task is already completed"):
            self.task.mark_completed()

    def test_update_priority_with_valid_priority_should_change_priority(self):
        """Test mise à jour priorité valide"""
        self.task.update_priority(Priority.HIGH)
        
        assert self.task.priority == Priority.HIGH

    def test_update_priority_with_invalid_type_should_raise_error(self):
        """Test mise à jour priorité type invalide lève erreur"""
        with pytest.raises(TypeError, match="Priority must be a Priority enum"):
            self.task.update_priority("high")

    def test_update_priority_on_completed_task_should_raise_error(self):
        """Test mise à jour priorité tâche terminée lève erreur"""
        self.task.mark_completed()
        
        with pytest.raises(ValueError, match="Cannot update priority of completed task"):
            self.task.update_priority(Priority.HIGH)

    def test_assign_to_project_with_valid_id_should_set_project_id(self):
        """Test assignation à un projet"""
        project_id = 123456.789
        self.task.assign_to_project(project_id)
        
        assert self.task.project_id == project_id

    def test_assign_to_project_with_invalid_type_should_raise_error(self):
        """Test assignation projet type invalide lève erreur"""
        with pytest.raises(TypeError, match="Project ID must be a number"):
            self.task.assign_to_project("invalid")

    @pytest.mark.parametrize("priority", [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.URGENT])
    def test_update_priority_with_all_valid_priorities(self, priority):
        """Test mise à jour avec toutes les priorités valides"""
        self.task.update_priority(priority)
        
        assert self.task.priority == priority


class TestTaskSerialization:
    """Tests de sérialisation JSON"""

    def setup_method(self):
        self.task = Task(
            "Tâche complexe",
            "Description avec caractères spéciaux éàç",
            Priority.HIGH
        )
        self.task.assign_to_project(987654.321)

    def test_to_dict_should_contain_all_required_fields(self):
        """Test conversion en dictionnaire"""
        task_dict = self.task.to_dict()
        
        required_fields = ["id", "title", "description", "priority", "status", "created_at", "completed_at", "project_id"]
        for field in required_fields:
            assert field in task_dict

    def test_to_dict_should_serialize_enums_as_strings(self):
        """Test sérialisation enums en strings"""
        task_dict = self.task.to_dict()
        
        assert isinstance(task_dict["priority"], str)
        assert isinstance(task_dict["status"], str)
        assert task_dict["priority"] == "high"
        assert task_dict["status"] == "todo"

    def test_to_dict_should_serialize_datetime_as_iso_string(self):
        """Test sérialisation datetime en ISO string"""
        task_dict = self.task.to_dict()
        
        assert isinstance(task_dict["created_at"], str)
        datetime.fromisoformat(task_dict["created_at"])

    def test_to_dict_completed_task_should_include_completed_at(self):
        """Test sérialisation tâche terminée inclut completed_at"""
        self.task.mark_completed()
        task_dict = self.task.to_dict()
        
        assert task_dict["completed_at"] is not None
        assert isinstance(task_dict["completed_at"], str)
        datetime.fromisoformat(task_dict["completed_at"])

    def test_from_dict_should_recreate_equivalent_task(self):
        """Test recréation depuis dictionnaire"""
        original_dict = self.task.to_dict()
        recreated_task = Task.from_dict(original_dict)
        
        assert recreated_task.id == self.task.id
        assert recreated_task.title == self.task.title
        assert recreated_task.description == self.task.description
        assert recreated_task.priority == self.task.priority
        assert recreated_task.status == self.task.status
        assert recreated_task.project_id == self.task.project_id

    def test_from_dict_with_missing_required_field_should_raise_error(self):
        """Test recréation avec champ manquant lève erreur"""
        incomplete_dict = {"title": "Test"}
        
        with pytest.raises(ValueError, match="Missing required field"):
            Task.from_dict(incomplete_dict)

    def test_from_dict_with_invalid_priority_should_raise_error(self):
        """Test recréation avec priorité invalide lève erreur"""
        invalid_dict = {
            "id": 123456.789,
            "title": "Test",
            "description": "Test",
            "priority": "invalid_priority",
            "status": "todo",
            "created_at": "2024-01-01T00:00:00.000000"
        }
        
        with pytest.raises(ValueError, match="Invalid priority"):
            Task.from_dict(invalid_dict)

    def test_from_dict_with_invalid_status_should_raise_error(self):
        """Test recréation avec statut invalide lève erreur"""
        invalid_dict = {
            "id": 123456.789,
            "title": "Test",
            "description": "Test", 
            "priority": "medium",
            "status": "invalid_status",
            "created_at": "2024-01-01T00:00:00.000000"
        }
        
        with pytest.raises(ValueError, match="Invalid status"):
            Task.from_dict(invalid_dict)

    def test_from_dict_with_invalid_data_type_should_raise_error(self):
        """Test recréation avec type données invalide lève erreur"""
        with pytest.raises(TypeError, match="Data must be a dictionary"):
            Task.from_dict("invalid_data")

    def test_task_equality_should_be_based_on_id(self):
        """Test égalité tâches basée sur ID"""
        task1 = Task("Test 1")
        task2 = Task("Test 2")
        task3_dict = task1.to_dict()
        task3 = Task.from_dict(task3_dict)
        
        assert task1 != task2
        assert task1 == task3

    def test_task_hash_should_be_based_on_id(self):
        """Test hash tâches basé sur ID"""
        task1 = Task("Test 1")
        task2_dict = task1.to_dict()
        task2 = Task.from_dict(task2_dict)
        
        assert hash(task1) == hash(task2)

    def test_task_repr_should_contain_meaningful_info(self):
        """Test représentation string tâche"""
        repr_str = repr(self.task)
        
        assert "Task" in repr_str
        assert str(self.task.id) in repr_str
        assert self.task.title in repr_str
        assert self.task.status.value in repr_str
