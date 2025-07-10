import pytest
from unittest.mock import patch, Mock, mock_open
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority


class TestEmailService:
    """Tests du service email avec mocks"""

    def setup_method(self):
        self.email_service = EmailService()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        """Test envoi rappel réussi"""
        # TODO: Configurez le mock SMTP
        # TODO: Appelez send_task_reminder
        # TODO: Vérifiez que l'email est "envoyé"
        pass

    def test_send_task_reminder_invalid_email(self):
        """Test envoi avec email invalide"""
        # TODO: Testez avec un email sans @
        # TODO: Vérifiez qu'une exception est levée
        pass


class TestReportService:
    """Tests du service de rapports"""

    def setup_method(self):
        self.report_service = ReportService()
        # TODO: Créez une liste de tâches de test
        pass

    @patch('src.task_manager.services.datetime')
    def test_generate_daily_report_fixed_date(self, mock_datetime):
        """Test génération rapport avec date fixe"""
        # TODO: Configurez mock_datetime pour une date fixe
        # TODO: Générez le rapport
        # TODO: Vérifiez la structure du rapport
        pass

    @patch('builtins.open', new_callable=mock_open)
    def test_export_tasks_csv(self, mock_file):
        """Test export CSV"""
        # TODO: Exportez les tâches
        # TODO: Vérifiez que le fichier est ouvert
        # TODO: Vérifiez qu'il y a bien écriture
        pass