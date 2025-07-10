from datetime import datetime
from enum import Enum


class Priority(Enum):
    # TODO: Définissez les priorités (LOW, MEDIUM, HIGH, URGENT)
    pass


class Status(Enum):
    # TODO: Définissez les statuts (TODO, IN_PROGRESS, DONE, CANCELLED)
    pass


class Task:
    """Une tâche avec toutes ses propriétés"""
    
    def __init__(self, title, description="", priority=Priority.MEDIUM):
        # TODO: Validez les paramètres
        # - title non vide
        # - priority est bien une Priority
        # TODO: Initialisez les attributs
        # - id unique (utilisez time.time() ou uuid)
        # - created_at avec datetime.now()
        # - status à TODO par défaut
        # - project_id à None
        pass
    
    def mark_completed(self):
        # TODO: Changez le statut à DONE
        # TODO: Ajoutez completed_at avec datetime.now()
        pass
    
    def update_priority(self, new_priority):
        # TODO: Validez et mettez à jour la priorité
        pass
    
    def assign_to_project(self, project_id):
        # TODO: Assignez la tâche à un projet
        pass
    
    def to_dict(self):
        # TODO: Retournez un dictionnaire pour la sérialisation JSON
        # Gérez la conversion des Enum et datetime
        pass
    
    @classmethod
    def from_dict(cls, data):
        # TODO: Créez une Task depuis un dictionnaire
        # Gérez la conversion des string vers Enum et datetime
        pass