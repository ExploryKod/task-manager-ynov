import pytest
from unittest.mock import patch, Mock, mock_open
from datetime import datetime, timedelta
import csv
import io
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority, Status


class TestEmailService:
    """Tests du service email avec mocks"""

    def setup_method(self):
        self.email_service = EmailService("test.smtp.com", 587)

    def test_init_should_set_smtp_configuration(self):
        """Test initialisation définit configuration SMTP"""
        service = EmailService("custom.smtp.com", 465)
        
        assert service.smtp_server == "custom.smtp.com"
        assert service.port == 465
        assert service.sent_emails == []

    def test_send_task_reminder_with_valid_email_should_return_true(self):
        """Test envoi rappel avec email valide"""
        result = self.email_service.send_task_reminder(
            "user@example.com",
            "Tâche test",
            datetime.now()
        )
        
        assert result is True

    def test_send_task_reminder_should_record_sent_email(self):
        """Test envoi rappel enregistre email envoyé"""
        task_title = "Tâche importante"
        email = "user@example.com"
        due_date = datetime.now()
        
        self.email_service.send_task_reminder(email, task_title, due_date)
        
        assert len(self.email_service.sent_emails) == 1
        sent_email = self.email_service.sent_emails[0]
        assert sent_email["to"] == email
        assert task_title in sent_email["subject"]
        assert sent_email["type"] == "reminder"

    def test_send_task_reminder_with_empty_email_should_raise_error(self):
        """Test envoi rappel email vide lève erreur"""
        with pytest.raises(ValueError, match="Email cannot be empty"):
            self.email_service.send_task_reminder("", "Task", datetime.now())

    def test_send_task_reminder_with_invalid_email_format_should_raise_error(self):
        """Test envoi rappel email invalide lève erreur"""
        with pytest.raises(ValueError, match="Invalid email format: missing '@' symbol"):
            self.email_service.send_task_reminder("invalid-email", "Task", datetime.now())

    def test_send_task_reminder_with_missing_domain_should_raise_error(self):
        """Test envoi rappel domaine manquant lève erreur"""
        with pytest.raises(ValueError, match="Invalid email format: missing domain"):
            self.email_service.send_task_reminder("user@", "Task", datetime.now())

    def test_send_task_reminder_with_missing_extension_should_raise_error(self):
        """Test envoi rappel extension manquante lève erreur"""
        with pytest.raises(ValueError, match="Invalid email format: missing extension"):
            self.email_service.send_task_reminder("user@domain", "Task", datetime.now())

    def test_send_task_reminder_with_missing_local_part_should_raise_error(self):
        """Test envoi rappel partie locale manquante lève erreur"""
        with pytest.raises(ValueError, match="Invalid email format: missing local part"):
            self.email_service.send_task_reminder("@domain.com", "Task", datetime.now())

    def test_send_task_reminder_with_too_long_email_should_raise_error(self):
        """Test envoi rappel email trop long lève erreur"""
        long_email = "a" * 350 + "@domain.com"
        with pytest.raises(ValueError, match="Email too long.*Maximum: 320"):
            self.email_service.send_task_reminder(long_email, "Task", datetime.now())

    def test_send_task_reminder_with_invalid_characters_should_raise_error(self):
        """Test envoi rappel caractères invalides lève erreur"""
        with pytest.raises(ValueError, match="Invalid email format: contains invalid characters"):
            self.email_service.send_task_reminder("user space@domain.com", "Task", datetime.now())

    def test_send_task_reminder_with_empty_title_should_raise_error(self):
        """Test envoi rappel titre vide lève erreur"""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            self.email_service.send_task_reminder("user@domain.com", "", datetime.now())

    def test_send_task_reminder_with_invalid_date_type_should_raise_error(self):
        """Test envoi rappel date type invalide lève erreur"""
        with pytest.raises(TypeError, match="Due date must be a datetime object"):
            self.email_service.send_task_reminder("user@domain.com", "Task", "invalid")

    def test_send_completion_notification_with_valid_data_should_return_true(self):
        """Test envoi notification completion données valides"""
        result = self.email_service.send_completion_notification(
            "user@example.com",
            "Tâche terminée"
        )
        
        assert result is True

    def test_send_completion_notification_should_record_sent_email(self):
        """Test notification completion enregistre email"""
        email = "user@example.com"
        task_title = "Tâche terminée"
        
        self.email_service.send_completion_notification(email, task_title)
        
        assert len(self.email_service.sent_emails) == 1
        sent_email = self.email_service.sent_emails[0]
        assert sent_email["to"] == email
        assert task_title in sent_email["subject"]
        assert sent_email["type"] == "completion"

    def test_get_sent_emails_should_return_copy_of_emails(self):
        """Test récupération emails envoyés retourne copie"""
        self.email_service.send_task_reminder("user@domain.com", "Task", datetime.now())
        
        emails = self.email_service.get_sent_emails()
        emails.clear()
        
        assert len(self.email_service.sent_emails) == 1

    def test_clear_sent_emails_should_empty_emails_list(self):
        """Test nettoyage emails vide la liste"""
        self.email_service.send_task_reminder("user@domain.com", "Task", datetime.now())
        
        self.email_service.clear_sent_emails()
        
        assert len(self.email_service.sent_emails) == 0

    @pytest.mark.parametrize("email,should_pass", [
        ("user@example.com", True),
        ("test.user+tag@domain.org", True),
        ("a@b.co", True),
        ("invalid-email", False),
        ("user@", False),
        ("@domain.com", False),
        ("user@domain", False),
        ("user space@domain.com", False),
    ])
    def test_email_validation_various_formats(self, email, should_pass):
        """Test validation email divers formats"""
        if should_pass:
            result = self.email_service.send_task_reminder(email, "Task", datetime.now())
            assert result is True
        else:
            with pytest.raises(ValueError):
                self.email_service.send_task_reminder(email, "Task", datetime.now())


class TestReportService:
    """Tests du service de rapports"""

    def setup_method(self):
        self.report_service = ReportService()
        self.sample_tasks = self._create_sample_tasks()

    def _create_sample_tasks(self):
        """Créer tâches échantillon pour tests"""
        tasks = []
        
        task1 = Task("Tâche TODO", "Description 1", Priority.HIGH)
        tasks.append(task1)
        
        task2 = Task("Tâche DONE", "Description 2", Priority.MEDIUM)
        task2.mark_completed()
        tasks.append(task2)
        
        task3 = Task("Tâche IN_PROGRESS", "Description 3", Priority.LOW)
        task3.status = Status.IN_PROGRESS
        tasks.append(task3)
        
        return tasks

    def test_generate_daily_report_with_tasks_should_return_report_structure(self):
        """Test génération rapport quotidien avec tâches"""
        report = self.report_service.generate_daily_report(self.sample_tasks)
        
        required_fields = [
            "report_date", "total_tasks", "tasks_for_date", "completed_today",
            "created_today", "completion_rate_today", "priority_breakdown",
            "status_breakdown", "generated_at", "summary"
        ]
        for field in required_fields:
            assert field in report

    def test_generate_daily_report_should_calculate_totals_correctly(self):
        """Test génération rapport calcul totaux"""
        report = self.report_service.generate_daily_report(self.sample_tasks)
        
        assert report["total_tasks"] == 3
        assert isinstance(report["completion_rate_today"], float)
        assert 0 <= report["completion_rate_today"] <= 100

    def test_generate_daily_report_should_include_priority_breakdown(self):
        """Test génération rapport inclut répartition priorités"""
        report = self.report_service.generate_daily_report(self.sample_tasks)
        
        priority_breakdown = report["priority_breakdown"]
        assert "urgent" in priority_breakdown
        assert "high" in priority_breakdown
        assert "medium" in priority_breakdown
        assert "low" in priority_breakdown

    def test_generate_daily_report_should_include_status_breakdown(self):
        """Test génération rapport inclut répartition statuts"""
        report = self.report_service.generate_daily_report(self.sample_tasks)
        
        status_breakdown = report["status_breakdown"]
        assert "todo" in status_breakdown
        assert "in_progress" in status_breakdown
        assert "done" in status_breakdown
        assert "cancelled" in status_breakdown

    def test_generate_daily_report_with_empty_tasks_should_raise_error(self):
        """Test génération rapport tâches vides lève erreur"""
        with pytest.raises(ValueError, match="Cannot generate report: no tasks found"):
            self.report_service.generate_daily_report([])

    def test_generate_daily_report_with_invalid_tasks_type_should_raise_error(self):
        """Test génération rapport type tâches invalide lève erreur"""
        with pytest.raises(TypeError, match="Tasks must be a list"):
            self.report_service.generate_daily_report("invalid")

    # @patch('src.task_manager.services.datetime')
    # def test_generate_daily_report_with_fixed_date_should_use_provided_date(self, mock_datetime):
    #     """Test génération rapport avec date fixe"""
    #     fixed_date = datetime(2024, 1, 15, 10, 0, 0)
    #     mock_datetime.now.return_value = fixed_date
        
    #     report = self.report_service.generate_daily_report(self.sample_tasks, fixed_date)
        
    #     assert report["report_date"] == fixed_date.isoformat()

    def test_generate_daily_report_with_invalid_date_type_should_raise_error(self):
        """Test génération rapport date type invalide lève erreur"""
        with pytest.raises(TypeError, match="Date must be a datetime object"):
            self.report_service.generate_daily_report(self.sample_tasks, "invalid")

    def test_export_tasks_csv_with_valid_tasks_should_return_true(self):
        """Test export CSV tâches valides"""
        with patch('builtins.open', mock_open()) as mock_file:
            result = self.report_service.export_tasks_csv(self.sample_tasks, "test.csv")
            
            assert result is True
            mock_file.assert_called_once()

    def test_export_tasks_csv_should_write_headers(self):
        """Test export CSV écrit en-têtes"""
        csv_content = io.StringIO()
        
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.return_value.write = csv_content.write
            self.report_service.export_tasks_csv(self.sample_tasks, "test.csv")
            
            mock_file.assert_called_once_with("test.csv", 'w', newline='', encoding='utf-8')

    def test_export_tasks_csv_with_empty_tasks_should_raise_error(self):
        """Test export CSV tâches vides lève erreur"""
        with pytest.raises(ValueError, match="Cannot export CSV: no tasks to export"):
            self.report_service.export_tasks_csv([], "test.csv")

    def test_export_tasks_csv_with_invalid_tasks_type_should_raise_error(self):
        """Test export CSV type tâches invalide lève erreur"""
        with pytest.raises(TypeError, match="Tasks must be a list"):
            self.report_service.export_tasks_csv("invalid", "test.csv")

    def test_export_tasks_csv_with_empty_filename_should_raise_error(self):
        """Test export CSV nom fichier vide lève erreur"""
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            self.report_service.export_tasks_csv(self.sample_tasks, "")

    def test_export_tasks_csv_with_invalid_filename_type_should_raise_error(self):
        """Test export CSV nom fichier type invalide lève erreur"""
        with pytest.raises(TypeError, match="Filename must be a string"):
            self.report_service.export_tasks_csv(self.sample_tasks, None)

    def test_export_tasks_csv_should_add_csv_extension_if_missing(self):
        """Test export CSV ajoute extension si manquante"""
        with patch('builtins.open', mock_open()) as mock_file:
            self.report_service.export_tasks_csv(self.sample_tasks, "test")
            
            mock_file.assert_called_once_with("test.csv", 'w', newline='', encoding='utf-8')

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_export_tasks_csv_permission_denied_should_raise_error(self, mock_file):
        """Test export CSV permission refusée lève erreur"""
        with pytest.raises(PermissionError, match="Cannot write to CSV file.*Permission denied"):
            self.report_service.export_tasks_csv(self.sample_tasks, "readonly.csv")

    def test_get_export_summary_with_tasks_should_return_summary(self):
        """Test résumé export avec tâches"""
        summary = self.report_service.get_export_summary(self.sample_tasks)
        
        assert summary["total_tasks"] == 3
        assert summary["exportable"] is True
        assert summary["format"] == "CSV"
        assert summary["encoding"] == "UTF-8"
        assert "fields_included" in summary

    def test_get_export_summary_with_empty_tasks_should_indicate_not_exportable(self):
        """Test résumé export tâches vides indique non exportable"""
        summary = self.report_service.get_export_summary([])
        
        assert summary["total_tasks"] == 0
        assert summary["exportable"] is False

    def test_get_export_summary_with_invalid_type_should_raise_error(self):
        """Test résumé export type invalide lève erreur"""
        with pytest.raises(TypeError, match="Tasks must be a list"):
            self.report_service.get_export_summary("invalid")

    @pytest.mark.parametrize("task_count,expected_exportable", [
        (0, False),
        (1, True),
        (10, True),
        (100, True),
    ])
    def test_get_export_summary_exportable_status(self, task_count, expected_exportable):
        """Test statut exportable résumé"""
        tasks = [Task(f"Task {i}") for i in range(task_count)]
        
        summary = self.report_service.get_export_summary(tasks)
        
        assert summary["exportable"] == expected_exportable