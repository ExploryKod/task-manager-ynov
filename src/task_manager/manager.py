# src/task_manager/manager.py
import json
import os
from typing import List, Optional, Dict, Any, Union
from .task import Task, Priority, Status


class TaskManager:
    """Gestionnaire principal des tâches"""

    MAX_TASKS_PER_PROJECT = 100
    MAX_JSON_FILES = 150

    def __init__(self, storage_file: str = "tasks.json") -> None:
        self._tasks: List[Task] = []
        self._storage_file: str = storage_file
        self._validate_storage_environment()

    def add_task(
        self, 
        title: str, 
        description: str = "", 
        priority: Priority = Priority.MEDIUM
    ) -> float:
        task = Task(title, description, priority)
        self._tasks.append(task)
        return task.id

    def get_task(self, task_id: Union[float, int, str, None]) -> Optional[Task]:
        if task_id is None:
            return None
        
        try:
            target_id = float(task_id)
        except (ValueError, TypeError):
            return None
        
        for task in self._tasks:
            if task.id == target_id:
                return task
        
        return None

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        if not isinstance(status, Status):
            raise TypeError(f"Status must be a Status enum, got {type(status)}")
        
        return [task for task in self._tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        if not isinstance(priority, Priority):
            raise TypeError(f"Priority must be a Priority enum, got {type(priority)}")
        
        return [task for task in self._tasks if task.priority == priority]

    def delete_task(self, task_id: Union[float, int, str, None]) -> bool:
        if task_id is None:
            return False
        
        try:
            target_id = float(task_id)
        except (ValueError, TypeError):
            return False
        
        for i, task in enumerate(self._tasks):
            if task.id == target_id:
                del self._tasks[i]
                return True
        
        return False

    def save_to_file(self, filename: Optional[str] = None) -> None:
        target_file = filename or self._storage_file
        
        self._validate_json_file_limits()
        
        try:
            data = {
                "tasks": [task.to_dict() for task in self._tasks],
                "metadata": {
                    "total_tasks": len(self._tasks),
                    "saved_at": self._get_current_time_iso()
                }
            }
            
            with open(target_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                
        except PermissionError as e:
            raise PermissionError(f"Cannot write to file '{target_file}': {str(e)}. Check file permissions.")
        except OSError as e:
            raise OSError(f"File system error while saving '{target_file}': {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while saving tasks: {str(e)}")

    def load_from_file(self, filename: Optional[str] = None) -> None:
        target_file = filename or self._storage_file
        
        if not os.path.exists(target_file):
            self._tasks = []
            return
        
        try:
            with open(target_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if not isinstance(data, dict):
                raise ValueError(f"Invalid JSON structure in '{target_file}': expected object, got {type(data)}")
            
            tasks_data = data.get("tasks", [])
            if not isinstance(tasks_data, list):
                raise ValueError(f"Invalid tasks format in '{target_file}': expected array, got {type(tasks_data)}")
            
            loaded_tasks = []
            for i, task_data in enumerate(tasks_data):
                try:
                    task = Task.from_dict(task_data)
                    loaded_tasks.append(task)
                except Exception as e:
                    raise ValueError(f"Invalid task data at index {i} in '{target_file}': {str(e)}")
            
            self._tasks = loaded_tasks
            
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON format in file '{target_file}'. File may be corrupted.", 
                e.doc, 
                e.pos
            )
        except PermissionError as e:
            raise PermissionError(f"Cannot read file '{target_file}': {str(e)}. Check file permissions.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while loading tasks: {str(e)}")

    def get_statistics(self) -> Dict[str, Any]:
        total_tasks = len(self._tasks)
        
        if total_tasks == 0:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "pending_tasks": 0,
                "in_progress_tasks": 0,
                "cancelled_tasks": 0,
                "completion_rate": 0.0,
                "priority_distribution": {
                    "low": 0,
                    "medium": 0,
                    "high": 0,
                    "urgent": 0
                },
                "status_distribution": {
                    "todo": 0,
                    "in_progress": 0,
                    "done": 0,
                    "cancelled": 0
                },
                "message": "No tasks found. Create tasks to see statistics.",
                "generated_at": self._get_current_time_iso()
            }
        
        completed_tasks = len([t for t in self._tasks if t.status == Status.DONE])
        pending_tasks = len([t for t in self._tasks if t.status == Status.TODO])
        in_progress_tasks = len([t for t in self._tasks if t.status == Status.IN_PROGRESS])
        cancelled_tasks = len([t for t in self._tasks if t.status == Status.CANCELLED])
        
        completion_rate = (completed_tasks / total_tasks) * 100.0
        
        priority_stats = {
            "low": len([t for t in self._tasks if t.priority == Priority.LOW]),
            "medium": len([t for t in self._tasks if t.priority == Priority.MEDIUM]),
            "high": len([t for t in self._tasks if t.priority == Priority.HIGH]),
            "urgent": len([t for t in self._tasks if t.priority == Priority.URGENT])
        }
        
        status_stats = {
            "todo": pending_tasks,
            "in_progress": in_progress_tasks,
            "done": completed_tasks,
            "cancelled": cancelled_tasks
        }
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "cancelled_tasks": cancelled_tasks,
            "completion_rate": round(completion_rate, 2),
            "priority_distribution": priority_stats,
            "status_distribution": status_stats,
            "message": f"{completion_rate:.1f}% completion rate",
            "generated_at": self._get_current_time_iso()
        }

    def get_all_tasks(self) -> List[Task]:
        return self._tasks.copy()

    def clear_all_tasks(self) -> None:
        self._tasks.clear()

    def get_task_count(self) -> int:
        return len(self._tasks)

    def _validate_storage_environment(self) -> None:
        storage_dir = os.path.dirname(self._storage_file) or "."
        
        if not os.path.exists(storage_dir):
            try:
                os.makedirs(storage_dir, exist_ok=True)
            except OSError as e:
                raise OSError(f"Cannot create storage directory '{storage_dir}': {str(e)}")

    def _validate_json_file_limits(self) -> None:
        storage_dir = os.path.dirname(self._storage_file) or "."
        
        try:
            existing_json_files = [
                f for f in os.listdir(storage_dir) 
                if f.endswith('.json')
            ]
            
            if len(existing_json_files) >= self.MAX_JSON_FILES:
                raise ValueError(
                    f"Maximum number of JSON files exceeded: {len(existing_json_files)}. "
                    f"Maximum allowed: {self.MAX_JSON_FILES}. "
                    f"Please clean up old files before saving."
                )
                
        except OSError:
            pass

    def _get_current_time_iso(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()

    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self):
        return iter(self._tasks)

    def __repr__(self) -> str:
        return f"TaskManager(tasks={len(self._tasks)}, storage='{self._storage_file}')"