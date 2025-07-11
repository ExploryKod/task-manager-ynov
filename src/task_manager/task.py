from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import time
import re


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    
    def __str__(self) -> str:
        return self.value


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    
    def __str__(self) -> str:
        return self.value


class Task:
    """Une tâche avec toutes ses propriétés"""
    
    MAX_TITLE_LENGTH = 100
    MIN_TITLE_LENGTH = 1
    
    def __init__(
        self, 
        title: str, 
        description: str = "", 
        priority: Priority = Priority.MEDIUM
    ) -> None:
        self._validate_title(title)
        self._validate_priority(priority)
        
        self.id: float = time.time()
        self.title: str = title.strip()
        self.description: str = description.strip()
        self.priority: Priority = priority
        self.created_at: datetime = datetime.now()
        self.status: Status = Status.TODO
        self.completed_at: Optional[datetime] = None
        self.project_id: Optional[float] = None
    
    def mark_completed(self) -> None:
        if self.status == Status.DONE:
            raise ValueError("Task is already completed")
        
        self.status = Status.DONE
        self.completed_at = datetime.now()
    
    def update_priority(self, new_priority: Priority) -> None:
        if not isinstance(new_priority, Priority):
            raise TypeError(f"Priority must be a Priority enum, got {type(new_priority)}")
        
        if self.status == Status.DONE:
            raise ValueError("Cannot update priority of completed task")
        
        self.priority = new_priority
    
    def assign_to_project(self, project_id: float) -> None:
        if not isinstance(project_id, (int, float)):
            raise TypeError(f"Project ID must be a number, got {type(project_id)}")
        
        self.project_id = float(project_id)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "project_id": self.project_id if self.project_id else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        
        required_fields = ["id", "title", "priority", "status", "created_at"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        task = cls.__new__(cls)
        
        task.id = float(data["id"])
        task.title = data["title"]
        task.description = data.get("description", "")
        
        try:
            task.priority = Priority[data["priority"].upper()]
        except KeyError:
            raise ValueError(f"Invalid priority: {data['priority']}")
        
        try:
            task.status = Status[data["status"].upper()]
        except KeyError:
            raise ValueError(f"Invalid status: {data['status']}")
        
        task.created_at = datetime.fromisoformat(data["created_at"])
        
        task.completed_at = (
            datetime.fromisoformat(data["completed_at"]) 
            if data.get("completed_at") 
            else None
        )
        
        task.project_id = float(data["project_id"]) if data.get("project_id") else None
        
        return task
    
    def _validate_title(self, title: str) -> None:
        if not isinstance(title, str):
            raise TypeError(f"Title must be a string, got {type(title)}")
        
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        
        clean_title = title.strip()
        
        if len(clean_title) < self.MIN_TITLE_LENGTH:
            raise ValueError(f"Title must be at least {self.MIN_TITLE_LENGTH} character")
        
        if len(clean_title) > self.MAX_TITLE_LENGTH:
            raise ValueError(f"Title cannot exceed {self.MAX_TITLE_LENGTH} characters, got {len(clean_title)}")
        
        if re.search(r'[<>]', clean_title):
            raise ValueError("Title contains invalid characters ('<', '>'). Please remove HTML tags for security")
    
    def _validate_priority(self, priority: Priority) -> None:
        if not isinstance(priority, Priority):
            raise TypeError(f"Priority must be a Priority enum, got {type(priority)}")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value})"