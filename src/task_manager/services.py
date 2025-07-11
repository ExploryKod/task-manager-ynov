import smtplib
import csv
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from .task import Task, Status, Priority


class EmailService:
    """Service d'envoi d'emails (à mocker dans les tests)"""

    MAX_EMAIL_LENGTH = 320
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", port: int = 587) -> None:
        self.smtp_server: str = smtp_server
        self.port: int = port
        self.sent_emails: List[Dict[str, Any]] = []

    def send_task_reminder(self, email: str, task_title: str, due_date: datetime) -> bool:
        self._validate_email(email)
        self._validate_task_title(task_title)
        
        if not isinstance(due_date, datetime):
            raise TypeError(f"Due date must be a datetime object, got {type(due_date)}")
        
        email_data = {
            "to": email,
            "subject": f"Task Reminder: {task_title}",
            "body": f"Reminder: Your task '{task_title}' is due on {due_date.strftime('%Y-%m-%d %H:%M')}",
            "sent_at": datetime.now().isoformat(),
            "type": "reminder"
        }
        
        self._simulate_email_sending(email_data)
        return True

    def send_completion_notification(self, email: str, task_title: str) -> bool:
        self._validate_email(email)
        self._validate_task_title(task_title)
        
        email_data = {
            "to": email,
            "subject": f"Task Completed: {task_title}",
            "body": f"Congratulations! Your task '{task_title}' has been marked as completed.",
            "sent_at": datetime.now().isoformat(),
            "type": "completion"
        }
        
        self._simulate_email_sending(email_data)
        return True

    def _validate_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError(f"Email must be a string, got {type(email)}")
        
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        
        email = email.strip()
        
        if len(email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(f"Email too long: {len(email)} characters. Maximum: {self.MAX_EMAIL_LENGTH}")
        
        if '@' not in email:
            raise ValueError(f"Invalid email format: missing '@' symbol in '{email}'")
        
        local_part, domain_part = email.split('@', 1)
        
        if not local_part:
            raise ValueError(f"Invalid email format: missing local part in '{email}'")
        
        if not domain_part:
            raise ValueError(f"Invalid email format: missing domain in '{email}'")
        
        if '.' not in domain_part:
            raise ValueError(f"Invalid email format: missing extension in '{email}'")
        
        if re.search(r'[<>"\s]', email):
            raise ValueError(f"Invalid email format: contains invalid characters in '{email}'")

    def _validate_task_title(self, task_title: str) -> None:
        if not isinstance(task_title, str):
            raise TypeError(f"Task title must be a string, got {type(task_title)}")
        
        if not task_title or not task_title.strip():
            raise ValueError("Task title cannot be empty")

    def _simulate_email_sending(self, email_data: Dict[str, Any]) -> None:
        self.sent_emails.append(email_data)
        print(f"[EMAIL SENT] {email_data['subject']} to {email_data['to']}")

    def get_sent_emails(self) -> List[Dict[str, Any]]:
        return self.sent_emails.copy()

    def clear_sent_emails(self) -> None:
        self.sent_emails.clear()


class ReportService:
    """Service de génération de rapports"""

    def generate_daily_report(
        self, 
        tasks: List[Task], 
        date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        if not isinstance(tasks, list):
            raise TypeError(f"Tasks must be a list, got {type(tasks)}")
        
        if len(tasks) == 0:
            raise ValueError("Cannot generate report: no tasks found. At least one task is required.")
        
        report_date = date if date is not None else datetime.now()
        
        if not isinstance(report_date, datetime):
            raise TypeError(f"Date must be a datetime object, got {type(report_date)}")
        
        tasks_for_date = self._filter_tasks_by_date(tasks, report_date)
        
        completed_today = len([t for t in tasks_for_date if t.status == Status.DONE])
        created_today = len([t for t in tasks_for_date if t.created_at.date() == report_date.date()])
        
        priority_breakdown = {
            "urgent": len([t for t in tasks_for_date if t.priority == Priority.URGENT]),
            "high": len([t for t in tasks_for_date if t.priority == Priority.HIGH]),
            "medium": len([t for t in tasks_for_date if t.priority == Priority.MEDIUM]),
            "low": len([t for t in tasks_for_date if t.priority == Priority.LOW])
        }
        
        status_breakdown = {
            "todo": len([t for t in tasks_for_date if t.status == Status.TODO]),
            "in_progress": len([t for t in tasks_for_date if t.status == Status.IN_PROGRESS]),
            "done": len([t for t in tasks_for_date if t.status == Status.DONE]),
            "cancelled": len([t for t in tasks_for_date if t.status == Status.CANCELLED])
        }
        
        return {
            "report_date": report_date.isoformat(),
            "total_tasks": len(tasks),
            "tasks_for_date": len(tasks_for_date),
            "completed_today": completed_today,
            "created_today": created_today,
            "completion_rate_today": (completed_today / len(tasks_for_date) * 100) if tasks_for_date else 0,
            "priority_breakdown": priority_breakdown,
            "status_breakdown": status_breakdown,
            "generated_at": datetime.now().isoformat(),
            "summary": f"Daily report for {report_date.strftime('%Y-%m-%d')}: {completed_today} tasks completed, {created_today} tasks created"
        }

    def export_tasks_csv(self, tasks: List[Task], filename: str) -> bool:
        if not isinstance(tasks, list):
            raise TypeError(f"Tasks must be a list, got {type(tasks)}")
        
        if not isinstance(filename, str):
            raise TypeError(f"Filename must be a string, got {type(filename)}")
        
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")
        
        if len(tasks) == 0:
            raise ValueError("Cannot export CSV: no tasks to export. At least one task is required.")
        
        filename = filename.strip()
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'title', 'description', 'priority', 'status',
                    'created_at', 'completed_at', 'project_id'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for task in tasks:
                    row = {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'priority': task.priority.value,
                        'status': task.status.value,
                        'created_at': task.created_at.isoformat(),
                        'completed_at': task.completed_at.isoformat() if task.completed_at else '',
                        'project_id': task.project_id if task.project_id else ''
                    }
                    writer.writerow(row)
            
            return True
            
        except PermissionError as e:
            raise PermissionError(f"Cannot write to CSV file '{filename}': {str(e)}. Check file permissions.")
        except OSError as e:
            raise OSError(f"File system error while exporting to '{filename}': {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while exporting CSV: {str(e)}")

    def _filter_tasks_by_date(self, tasks: List[Task], target_date: datetime) -> List[Task]:
        target_date_only = target_date.date()
        return [
            task for task in tasks
            if (task.created_at.date() == target_date_only or
                (task.completed_at and task.completed_at.date() == target_date_only))
        ]

    def get_export_summary(self, tasks: List[Task]) -> Dict[str, Any]:
        if not isinstance(tasks, list):
            raise TypeError(f"Tasks must be a list, got {type(tasks)}")
        
        return {
            "total_tasks": len(tasks),
            "exportable": len(tasks) > 0,
            "estimated_size_kb": len(tasks) * 0.5,
            "fields_included": [
                'id', 'title', 'description', 'priority', 'status',
                'created_at', 'completed_at', 'project_id'
            ],
            "format": "CSV",
            "encoding": "UTF-8"
        }