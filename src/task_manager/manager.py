# src/task_manager/manager.py
import json
from typing import List, Optional
from .task import Task, Priority, Status


class TaskManager:
    """Gestionnaire principal des tâches"""

    def __init__(self, storage_file="tasks.json"):
        # TODO: Initialisez la liste des tâches et le fichier de stockage
        pass

    def add_task(self, title, description="", priority=Priority.MEDIUM):
        # TODO: Créez et ajoutez une nouvelle tâche
        # TODO: Retournez l'ID de la tâche créée
        pass

    def get_task(self, task_id) -> Optional[Task]:
        # TODO: Trouvez une tâche par son ID
        pass

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        # TODO: Filtrez les tâches par statut
        pass

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        # TODO: Filtrez les tâches par priorité
        pass

    def delete_task(self, task_id) -> bool:
        # TODO: Supprimez une tâche
        # TODO: Retournez True si trouvée et supprimée, False sinon
        pass

    def save_to_file(self, filename=None):
        # TODO: Sauvegardez toutes les tâches en JSON
        # TODO: Gérez les erreurs d'écriture
        pass

    def load_from_file(self, filename=None):
        # TODO: Chargez les tâches depuis JSON
        # TODO: Gérez le cas du fichier inexistant
        pass

    def get_statistics(self):
        # TODO: Retournez un dictionnaire avec :
        # - total_tasks
        # - completed_tasks
        # - tasks_by_priority (dict)
        # - tasks_by_status (dict)
        pass