import smtplib
from datetime import datetime


class EmailService:
    """Service d'envoi d'emails (à mocker dans les tests)"""

    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        # TODO: Stockez la configuration SMTP
        pass

    def send_task_reminder(self, email, task_title, due_date):
        # TODO: Simulez l'envoi d'un email de rappel
        # TODO: Levez une exception si email invalide
        # TODO: Retournez True si succès
        pass

    def send_completion_notification(self, email, task_title):
        # TODO: Simulez l'envoi d'un email de confirmation
        pass


class ReportService:
    """Service de génération de rapports"""

    def generate_daily_report(self, tasks, date=None):
        # TODO: Générez un rapport quotidien
        # TODO: Utilisez datetime.now() si date=None
        # TODO: Retournez un dictionnaire avec les métriques du jour
        pass

    def export_tasks_csv(self, tasks, filename):
        # TODO: Exportez les tâches en CSV
        # TODO: Gérez les erreurs d'écriture
        pass