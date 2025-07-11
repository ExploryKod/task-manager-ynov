#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import EmailService


def main():
    print("=== Démonstration TaskManager ===\n")
    
    # TODO 1: Créez un gestionnaire
    print("1. Création du gestionnaire de tâches...")
    manager = TaskManager("demo_tasks.json")
    print(f"Gestionnaire créé avec stockage: {manager._storage_file}")
    print()
    
    # TODO 2: Ajoutez plusieurs tâches avec différentes priorités
    print("2. Ajout de plusieurs tâches avec différentes priorités...")
    
    # Tâche priorité URGENT
    task_id1 = manager.add_task(
        "Corriger bug critique en production", 
        "Le serveur principal ne répond plus",
        Priority.URGENT
    )
    print(f"Tâche URGENT ajoutée (ID: {task_id1:.3f})")
    
    # Tâche priorité HIGH
    task_id2 = manager.add_task(
        "Préparer présentation client",
        "Présentation pour le projet Q1",
        Priority.HIGH
    )
    print(f"Tâche HIGH ajoutée (ID: {task_id2:.3f})")
    
    # Tâche priorité MEDIUM (par défaut)
    task_id3 = manager.add_task(
        "Mettre à jour documentation",
        "Documentation API utilisateur"
    )
    print(f"Tâche MEDIUM ajoutée (ID: {task_id3:.3f})")
    
    # Tâche priorité LOW
    task_id4 = manager.add_task(
        "Optimiser les performances",
        "Améliorer temps de réponse",
        Priority.LOW
    )
    print(f"Tâche LOW ajoutée (ID: {task_id4:.3f})")
    
    print(f"\nTotal: {len(manager)} tâches ajoutées avec succès")
    print()
    
    # TODO 3: Marquez certaines comme terminées
    print("3. Marquage de certaines tâches comme terminées...")
    
    # Marquer la tâche URGENT comme terminée
    task_urgent = manager.get_task(task_id1)
    if task_urgent:
        task_urgent.mark_completed()
        print(f"Tâche URGENT terminée: '{task_urgent.title}'")
    
    # Marquer la tâche MEDIUM comme terminée  
    task_medium = manager.get_task(task_id3)
    if task_medium:
        task_medium.mark_completed()
        print(f"Tâche MEDIUM terminée: '{task_medium.title}'")
    
    print(f"Tâches terminées: {len([t for t in manager if t.status == Status.DONE])}/{len(manager)}")
    print()
    
    # TODO 4: Affichez les statistiques
    print("4. Affichage des statistiques...")
    stats = manager.get_statistics()
    
    print(f"Statistiques générales:")
    print(f"  - Total des tâches: {stats['total_tasks']}")
    print(f"  - Tâches terminées: {stats['completed_tasks']}")
    print(f"  - Tâches en attente: {stats['pending_tasks']}")
    print(f"  - Taux de completion: {stats['completion_rate']}%")
    
    print(f"\nRépartition par priorité:")
    for priority, count in stats['priority_distribution'].items():
        print(f"  - {priority.upper()}: {count} tâche(s)")
    
    print(f"\nRépartition par statut:")
    for status, count in stats['status_distribution'].items():
        print(f"  - {status.upper()}: {count} tâche(s)")
    
    print(f"\nMessage: {stats['message']}")
    print()
    
    # TODO 5: Sauvegardez dans un fichier
    print("5. Sauvegarde dans un fichier...")
    manager.save_to_file()
    print(f"Tâches sauvegardées dans: {manager._storage_file}")
    
    # Vérifier la taille du fichier
    import os
    if os.path.exists(manager._storage_file):
        file_size = os.path.getsize(manager._storage_file)
        print(f"Taille du fichier: {file_size} octets")
    print()
    
    # TODO 6: Rechargez et vérifiez
    print("6. Rechargement et vérification des données...")
    
    # Créer un nouveau gestionnaire qui charge depuis le fichier
    manager_reload = TaskManager("demo_tasks.json")
    manager_reload.load_from_file()  # Charger explicitement les données
    print(f"Nouveau gestionnaire créé et chargé depuis: {manager_reload._storage_file}")
    
    # Vérifier que les données ont été rechargées correctement
    print(f"Nombre de tâches rechargées: {len(manager_reload)}")
    
    # Vérifier les statistiques après rechargement
    stats_reload = manager_reload.get_statistics()
    print(f"Taux de completion après rechargement: {stats_reload['completion_rate']}%")
    
    # Afficher les tâches rechargées pour vérification
    print("\nTâches rechargées:")
    for task in manager_reload:
        status_symbol = "FINISHED" if task.status == Status.DONE else "UNFINISHED"
        print(f"  {status_symbol} [{task.priority.name}] {task.title} - {task.status.name}")
    
    # Vérifier que les données sont identiques
    original_stats = manager.get_statistics()
    if (len(manager) == len(manager_reload) and 
        original_stats['completion_rate'] == stats_reload['completion_rate']):
        print("\n Vérification réussie: Les données ont été sauvegardées et rechargées correctement!")
    else:
        print("\n Erreur: Les données rechargées ne correspondent pas aux données originales!")
    
    print()
    
    print("== Fin de la démonstration ==")


if __name__ == "__main__":
    main()