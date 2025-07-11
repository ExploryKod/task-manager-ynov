import pytest
import json
import tempfile
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.task_manager.task import Task, Priority, Status
from src.task_manager.manager import TaskManager
from src.task_manager.services import EmailService, ReportService
import datetime as dt


@pytest.fixture
def sample_task_minimal():
    """Fixture: tâche minimale pour tests basiques"""
    return Task("Tâche de test")


@pytest.fixture
def sample_task_complete():
    """Fixture: tâche complète avec tous les attributs"""
    task = Task(
        title="Compléter le rapport mensuel",
        description="Finaliser le rapport de performance pour janvier 2024",
        priority=Priority.HIGH
    )
    task.project_id = 1234567890.123
    return task


@pytest.fixture
def sample_completed_task():
    """Fixture: tâche déjà terminée"""
    task = Task("Tâche terminée", "Description de tâche terminée", Priority.MEDIUM)
    task.mark_completed()
    return task


@pytest.fixture
def sample_tasks_various_statuses():
    """Fixture: liste de tâches avec différents statuts"""
    tasks = []
    
    # Tâche TODO
    task_todo = Task("Tâche à faire", "Description TODO", Priority.HIGH)
    tasks.append(task_todo)
    
    # Tâche IN_PROGRESS  
    task_progress = Task("Tâche en cours", "Description en cours", Priority.MEDIUM)
    task_progress.status = Status.IN_PROGRESS
    tasks.append(task_progress)
    
    # Tâche DONE
    task_done = Task("Tâche terminée", "Description terminée", Priority.LOW)
    task_done.mark_completed()
    tasks.append(task_done)
    
    # Tâche CANCELLED
    task_cancelled = Task("Tâche annulée", "Description annulée", Priority.URGENT)
    task_cancelled.status = Status.CANCELLED
    tasks.append(task_cancelled)
    
    return tasks


@pytest.fixture
def sample_tasks_various_priorities():
    """Fixture: liste de tâches avec différentes priorités"""
    tasks = []
    
    for priority in Priority:
        task = Task(
            title=f"Tâche {priority.value}",
            description=f"Description pour priorité {priority.value}",
            priority=priority
        )
        tasks.append(task)
    
    return tasks


@pytest.fixture
def temp_json_file():
    """Fixture: fichier JSON temporaire pour tests"""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def task_manager_empty():
    """Fixture: gestionnaire de tâches vide"""
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    manager = TaskManager(temp_path)
    yield manager
    try:
        os.unlink(temp_path)
    except OSError:
        pass


@pytest.fixture
def task_manager_with_tasks():
    """Fixture: gestionnaire avec plusieurs tâches de test"""
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    manager = TaskManager(temp_path)
    
    # Ajouter diverses tâches
    manager.add_task("Tâche urgente", "Description urgente", Priority.URGENT)
    manager.add_task("Tâche normale", "Description normale", Priority.MEDIUM)
    manager.add_task("Tâche simple", "Description simple", Priority.LOW)
    
    # Marquer une tâche comme terminée
    task_id = manager.add_task("Tâche terminée", "Description terminée", Priority.HIGH)
    task = manager.get_task(task_id)
    if task:
        task.mark_completed()
    
    yield manager
    try:
        os.unlink(temp_path)
    except OSError:
        pass


@pytest.fixture
def email_service():
    """Fixture: service email pour tests"""
    return EmailService("test.smtp.com", 587)


@pytest.fixture
def report_service():
    """Fixture: service de rapports pour tests"""
    return ReportService()


@pytest.fixture
def valid_emails():
    """Fixture: liste d'emails valides pour tests"""
    return [
        "user@example.com",
        "test.user+tag@domain.org",
        "simple@test.fr",
        "a@b.co",
        "long.email.address@very-long-domain-name.com"
    ]


@pytest.fixture
def invalid_emails():
    """Fixture: liste d'emails invalides pour tests"""
    return [
        "invalid-email",
        "user@",
        "@domain.com",
        "user@domain",
        "user space@domain.com",
        "user<script>@domain.com",
        "",
        "a" * 350 + "@domain.com"  # Trop long
    ]


@pytest.fixture
def test_dates():
    """Fixture: dates de test pour différents scénarios"""
    now = datetime.now()
    return {
        "now": now,
        "yesterday": now - timedelta(days=1),
        "tomorrow": now + timedelta(days=1),
        "last_week": now - timedelta(weeks=1),
        "next_week": now + timedelta(weeks=1),
        "epoch": datetime(1970, 1, 1),
        "future": datetime(2099, 12, 31)
    }


@pytest.fixture
def boundary_test_values():
    """Fixture: valeurs pour tests aux frontières"""
    return {
        "title_lengths": {
            "empty": "",
            "whitespace": "   ",
            "min_valid": "A",
            "normal": "Titre normal",
            "max_valid": "A" * 100,
            "over_max": "A" * 101,
            "with_html": "<script>alert('xss')</script>",
            "with_symbols": "Titre avec @ & _ - caractères"
        },
        "email_lengths": {
            "min_valid": "a@b",
            "normal": "user@domain.com",
            "max_valid": "a" * 310 + "@test.com",
            "over_max": "a" * 320 + "@test.com"
        },
        "task_counts": {
            "zero": 0,
            "one": 1,
            "normal": 10,
            "large": 100,
            "max_per_project": 100,
            "over_max": 101
        }
    }


@pytest.fixture
def mock_file_system_limits():
    """Fixture: simulation des limites du système de fichiers"""
    return {
        "max_json_files": 150,
        "existing_files_at_limit": [f"file_{i}.json" for i in range(150)],
        "existing_files_over_limit": [f"file_{i}.json" for i in range(151)]
    }


@pytest.fixture
def fake_json_data():
    """Fixture: données JSON fake pour tests de persistence"""
    fake_data_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'fake_data.json')
    with open(fake_data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def task_statistics_scenarios():
    """Fixture: scénarios pour tests de statistiques"""
    return [
        {
            "name": "empty",
            "tasks": [],
            "expected_completion_rate": 0.0,
            "expected_message": "No tasks found"
        },
        {
            "name": "all_pending",
            "task_count": 5,
            "completed_count": 0,
            "expected_completion_rate": 0.0
        },
        {
            "name": "half_completed",
            "task_count": 4,
            "completed_count": 2,
            "expected_completion_rate": 50.0
        },
        {
            "name": "all_completed",
            "task_count": 3,
            "completed_count": 3,
            "expected_completion_rate": 100.0
        }
    ]


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Fixture automatique: nettoyage des fichiers de test"""
    test_files = []
    yield test_files
    
    for file_path in test_files:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except OSError:
            pass


class TaskBuilder:
    """Builder pattern pour créer des tâches de test personnalisées"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._title = "Test Task"
        self._description = "Test Description"
        self._priority = Priority.MEDIUM
        self._status = Status.TODO
        self._project_id = None
        self._completed = False
        return self
    
    def with_title(self, title: str):
        self._title = title
        return self
    
    def with_description(self, description: str):
        self._description = description
        return self
    
    def with_priority(self, priority: Priority):
        self._priority = priority
        return self
    
    def with_project_id(self, project_id: float):
        self._project_id = project_id
        return self
    
    def as_completed(self):
        self._completed = True
        return self
    
    def with_status(self, status: Status):
        self._status = status
        return self
    
    def build(self) -> Task:
        task = Task(self._title, self._description, self._priority)
        task.status = self._status
        if self._project_id:
            task.assign_to_project(self._project_id)
        if self._completed:
            task.mark_completed()
        return task


@pytest.fixture
def task_builder():
    """Fixture: builder pour créer des tâches personnalisées"""
    return TaskBuilder() 