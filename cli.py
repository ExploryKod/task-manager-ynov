#!/usr/bin/env python3
"""
Interface en ligne de commande pour TaskManager
"""
import argparse
import sys
import os
from datetime import datetime
from typing import Optional, List

# Ajouter le chemin src pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status


class Colors:
    """Couleurs pour l'affichage terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def disable():
        """Désactiver les couleurs"""
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''
        Colors.WHITE = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''
        Colors.END = ''


class TaskManagerCLI:
    """Interface CLI pour TaskManager"""
    
    def __init__(self, storage_file: str = "tasks_cli.json"):
        self.manager = TaskManager(storage_file)
        self.manager.load_from_file()
        
    def print_success(self, message: str):
        """Afficher un message de succès"""
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
        
    def print_error(self, message: str):
        """Afficher un message d'erreur"""
        print(f"{Colors.RED}✗ {message}{Colors.END}")
        
    def print_info(self, message: str):
        """Afficher un message d'information"""
        print(f"{Colors.BLUE}ℹ {message}{Colors.END}")
        
    def print_warning(self, message: str):
        """Afficher un message d'avertissement"""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")
        
    def get_priority_color(self, priority: Priority) -> str:
        """Retourner la couleur selon la priorité"""
        priority_colors = {
            Priority.LOW: Colors.GREEN,
            Priority.MEDIUM: Colors.YELLOW,
            Priority.HIGH: Colors.MAGENTA,
            Priority.URGENT: Colors.RED
        }
        return priority_colors.get(priority, Colors.WHITE)
    
    def get_status_symbol(self, status: Status) -> str:
        """Retourner le symbole selon le statut"""
        status_symbols = {
            Status.TODO: "○",
            Status.IN_PROGRESS: "◐",
            Status.DONE: "●",
            Status.CANCELLED: "✗"
        }
        return status_symbols.get(status, "?")
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> None:
        """Ajouter une nouvelle tâche"""
        try:
            priority_enum = Priority[priority.upper()]
            task_id = self.manager.add_task(title, description, priority_enum)
            self.manager.save_to_file()
            self.print_success(f"Tâche créée avec l'ID: {task_id:.3f}")
            self.print_info(f"Titre: {title}")
            if description:
                self.print_info(f"Description: {description}")
            self.print_info(f"Priorité: {priority_enum.name}")
        except KeyError:
            self.print_error(f"Priorité invalide: {priority}. Utilisez: low, medium, high, urgent")
        except Exception as e:
            self.print_error(f"Erreur lors de l'ajout de la tâche: {e}")
    
    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, 
                   limit: Optional[int] = None) -> None:
        """Lister les tâches avec filtres optionnels"""
        tasks = list(self.manager)
        
        if not tasks:
            self.print_warning("Aucune tâche trouvée.")
            return
        
        # Filtrer par statut
        if status:
            try:
                status_enum = Status[status.upper()]
                tasks = [t for t in tasks if t.status == status_enum]
            except KeyError:
                self.print_error(f"Statut invalide: {status}. Utilisez: todo, in_progress, done, cancelled")
                return
        
        # Filtrer par priorité
        if priority:
            try:
                priority_enum = Priority[priority.upper()]
                tasks = [t for t in tasks if t.priority == priority_enum]
            except KeyError:
                self.print_error(f"Priorité invalide: {priority}. Utilisez: low, medium, high, urgent")
                return
        
        # Limiter le nombre de résultats
        if limit and limit > 0:
            tasks = tasks[:limit]
        
        if not tasks:
            self.print_warning("Aucune tâche ne correspond aux critères.")
            return
        
        # Afficher les tâches
        print(f"\n{Colors.BOLD}📋 Liste des tâches ({len(tasks)} trouvée(s)):{Colors.END}")
        print("-" * 80)
        
        for task in tasks:
            priority_color = self.get_priority_color(task.priority)
            status_symbol = self.get_status_symbol(task.status)
            
            print(f"{status_symbol} {Colors.BOLD}ID: {task.id:.3f}{Colors.END}")
            print(f"  {Colors.CYAN}Titre:{Colors.END} {task.title}")
            if task.description:
                print(f"  {Colors.CYAN}Description:{Colors.END} {task.description}")
            print(f"  {Colors.CYAN}Priorité:{Colors.END} {priority_color}{task.priority.name}{Colors.END}")
            print(f"  {Colors.CYAN}Statut:{Colors.END} {task.status.name}")
            print(f"  {Colors.CYAN}Créé:{Colors.END} {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.completed_at:
                print(f"  {Colors.CYAN}Terminé:{Colors.END} {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 80)
    
    def complete_task(self, task_id: str) -> None:
        """Marquer une tâche comme terminée"""
        try:
            task = self.manager.get_task(task_id)
            if not task:
                self.print_error(f"Tâche avec l'ID {task_id} introuvable.")
                return
            
            if task.status == Status.DONE:
                self.print_warning(f"La tâche '{task.title}' est déjà terminée.")
                return
            
            task.mark_completed()
            self.manager.save_to_file()
            self.print_success(f"Tâche terminée: '{task.title}'")
            
        except Exception as e:
            self.print_error(f"Erreur lors de la finalisation de la tâche: {e}")
    
    def delete_task(self, task_id: str) -> None:
        """Supprimer une tâche"""
        try:
            task = self.manager.get_task(task_id)
            if not task:
                self.print_error(f"Tâche avec l'ID {task_id} introuvable.")
                return
            
            title = task.title
            if self.manager.delete_task(task_id):
                self.manager.save_to_file()
                self.print_success(f"Tâche supprimée: '{title}'")
            else:
                self.print_error(f"Impossible de supprimer la tâche avec l'ID {task_id}")
                
        except Exception as e:
            self.print_error(f"Erreur lors de la suppression de la tâche: {e}")
    
    def show_stats(self) -> None:
        """Afficher les statistiques"""
        stats = self.manager.get_statistics()
        
        print(f"\n{Colors.BOLD}📊 Statistiques TaskManager{Colors.END}")
        print("=" * 50)
        
        # Statistiques générales
        print(f"{Colors.CYAN}Statistiques générales:{Colors.END}")
        print(f"  Total des tâches: {Colors.BOLD}{stats['total_tasks']}{Colors.END}")
        print(f"  Tâches terminées: {Colors.GREEN}{stats['completed_tasks']}{Colors.END}")
        print(f"  Tâches en attente: {Colors.YELLOW}{stats['pending_tasks']}{Colors.END}")
        print(f"  Tâches en cours: {Colors.BLUE}{stats['in_progress_tasks']}{Colors.END}")
        print(f"  Tâches annulées: {Colors.RED}{stats['cancelled_tasks']}{Colors.END}")
        print(f"  Taux de completion: {Colors.BOLD}{stats['completion_rate']}%{Colors.END}")
        
        # Répartition par priorité
        print(f"\n{Colors.CYAN}Répartition par priorité:{Colors.END}")
        for priority, count in stats['priority_distribution'].items():
            priority_color = self.get_priority_color(Priority[priority.upper()])
            print(f"  {priority_color}{priority.upper()}:{Colors.END} {count} tâche(s)")
        
        # Répartition par statut
        print(f"\n{Colors.CYAN}Répartition par statut:{Colors.END}")
        for status, count in stats['status_distribution'].items():
            print(f"  {status.upper()}: {count} tâche(s)")
        
        print(f"\n{Colors.BLUE}Message: {stats['message']}{Colors.END}")
        print(f"{Colors.BLUE}Généré le: {stats['generated_at']}{Colors.END}")
    
    def save_data(self, filename: Optional[str] = None) -> None:
        """Sauvegarder les données"""
        try:
            if filename:
                self.manager.save_to_file(filename)
                self.print_success(f"Données sauvegardées dans: {filename}")
            else:
                self.manager.save_to_file()
                self.print_success("Données sauvegardées dans le fichier par défaut.")
        except Exception as e:
            self.print_error(f"Erreur lors de la sauvegarde: {e}")
    
    def load_data(self, filename: str) -> None:
        """Charger les données depuis un fichier"""
        try:
            if not os.path.exists(filename):
                self.print_error(f"Fichier introuvable: {filename}")
                return
            
            old_count = len(self.manager)
            self.manager.load_from_file(filename)
            new_count = len(self.manager)
            
            self.print_success(f"Données chargées depuis: {filename}")
            self.print_info(f"Tâches chargées: {new_count} (remplace {old_count} tâches précédentes)")
            
        except Exception as e:
            self.print_error(f"Erreur lors du chargement: {e}")
    
    def interactive_mode(self) -> None:
        """Mode interactif"""
        print(f"\n{Colors.BOLD}🎯 Mode interactif TaskManager{Colors.END}")
        print("Tapez 'help' pour voir les commandes disponibles, 'quit' pour quitter.\n")
        
        while True:
            try:
                command = input(f"{Colors.CYAN}TaskManager> {Colors.END}").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    self.print_info("Au revoir!")
                    break
                elif command.lower() == 'help':
                    self.print_interactive_help()
                elif command.lower() == 'list':
                    self.list_tasks()
                elif command.lower() == 'stats':
                    self.show_stats()
                elif command.lower() == 'save':
                    self.save_data()
                elif command.startswith('add '):
                    # Parsing simple pour add
                    parts = command[4:].strip().split('"')
                    if len(parts) >= 2:
                        title = parts[1]
                        description = parts[3] if len(parts) > 3 else ""
                        self.add_task(title, description)
                    else:
                        self.print_error("Format: add \"titre\" [\"description\"]")
                elif command.startswith('complete '):
                    task_id = command[9:].strip()
                    self.complete_task(task_id)
                elif command.startswith('delete '):
                    task_id = command[7:].strip()
                    self.delete_task(task_id)
                elif command.strip() == '':
                    continue
                else:
                    self.print_error(f"Commande inconnue: {command}")
                    self.print_info("Tapez 'help' pour voir les commandes disponibles.")
                    
            except KeyboardInterrupt:
                self.print_info("\nAu revoir!")
                break
            except Exception as e:
                self.print_error(f"Erreur: {e}")
    
    def print_interactive_help(self) -> None:
        """Afficher l'aide du mode interactif"""
        print(f"\n{Colors.BOLD}📖 Commandes disponibles:{Colors.END}")
        print("  list                     - Lister toutes les tâches")
        print("  add \"titre\" [\"description\"] - Ajouter une tâche")
        print("  complete <ID>            - Marquer une tâche comme terminée")
        print("  delete <ID>              - Supprimer une tâche")
        print("  stats                    - Afficher les statistiques")
        print("  save                     - Sauvegarder les données")
        print("  help                     - Afficher cette aide")
        print("  quit/exit/q              - Quitter le mode interactif")
        print()


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="TaskManager - Gestionnaire de tâches en ligne de commande",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s add "Faire les courses" "Acheter du pain et du lait" --priority high
  %(prog)s list --status todo --limit 5
  %(prog)s complete 1234.567
  %(prog)s delete 1234.567
  %(prog)s stats
  %(prog)s save backup.json
  %(prog)s load backup.json
  %(prog)s interactive
        """
    )
    
    parser.add_argument('--no-color', action='store_true', 
                       help='Désactiver les couleurs dans l\'affichage')
    parser.add_argument('--file', '-f', default='tasks_cli.json',
                       help='Fichier de stockage (défaut: tasks_cli.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande add
    add_parser = subparsers.add_parser('add', help='Ajouter une nouvelle tâche')
    add_parser.add_argument('title', help='Titre de la tâche')
    add_parser.add_argument('description', nargs='?', default='', help='Description de la tâche')
    add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high', 'urgent'],
                           default='medium', help='Priorité de la tâche')
    
    # Commande list
    list_parser = subparsers.add_parser('list', help='Lister les tâches')
    list_parser.add_argument('--status', '-s', choices=['todo', 'in_progress', 'done', 'cancelled'],
                            help='Filtrer par statut')
    list_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high', 'urgent'],
                            help='Filtrer par priorité')
    list_parser.add_argument('--limit', '-l', type=int, help='Limiter le nombre de résultats')
    
    # Commande complete
    complete_parser = subparsers.add_parser('complete', help='Marquer une tâche comme terminée')
    complete_parser.add_argument('task_id', help='ID de la tâche à terminer')
    
    # Commande delete
    delete_parser = subparsers.add_parser('delete', help='Supprimer une tâche')
    delete_parser.add_argument('task_id', help='ID de la tâche à supprimer')
    
    # Commande stats
    stats_parser = subparsers.add_parser('stats', help='Afficher les statistiques')
    
    # Commande save
    save_parser = subparsers.add_parser('save', help='Sauvegarder les données')
    save_parser.add_argument('filename', nargs='?', help='Nom du fichier de sauvegarde')
    
    # Commande load
    load_parser = subparsers.add_parser('load', help='Charger les données')
    load_parser.add_argument('filename', help='Nom du fichier à charger')
    
    # Commande interactive
    interactive_parser = subparsers.add_parser('interactive', help='Mode interactif')
    
    args = parser.parse_args()
    
    # Désactiver les couleurs si demandé
    if args.no_color:
        Colors.disable()
    
    # Créer l'instance CLI
    cli = TaskManagerCLI(args.file)
    
    # Exécuter la commande
    if args.command == 'add':
        cli.add_task(args.title, args.description, args.priority)
    elif args.command == 'list':
        cli.list_tasks(args.status, args.priority, args.limit)
    elif args.command == 'complete':
        cli.complete_task(args.task_id)
    elif args.command == 'delete':
        cli.delete_task(args.task_id)
    elif args.command == 'stats':
        cli.show_stats()
    elif args.command == 'save':
        cli.save_data(args.filename)
    elif args.command == 'load':
        cli.load_data(args.filename)
    elif args.command == 'interactive':
        cli.interactive_mode()
    else:
        # Aucune commande spécifiée, afficher l'aide
        parser.print_help()


if __name__ == '__main__':
    main() 