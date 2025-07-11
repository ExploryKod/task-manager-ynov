#!/usr/bin/env python3
"""
Démonstration de l'export vers différents formats
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import ExportService
import os


def main():
    print("=== Démonstration Export TaskManager ===\n")
    
    # Créer un gestionnaire avec des tâches de démonstration
    print("1. Création du gestionnaire et ajout de tâches de démonstration...")
    manager = TaskManager("demo_export_data.json")
    
    # Ajouter des tâches de test
    task_ids = []
    
    # Tâche urgente terminée
    task_id1 = manager.add_task(
        "Corriger bug critique production",
        "Bug empêchant les utilisateurs de se connecter",
        Priority.URGENT
    )
    task_ids.append(task_id1)
    manager.get_task(task_id1).mark_completed()
    
    # Tâche haute priorité en cours
    task_id2 = manager.add_task(
        "Développer API REST",
        "Développement de l'API pour l'application mobile",
        Priority.HIGH
    )
    task_ids.append(task_id2)
    manager.get_task(task_id2).status = Status.IN_PROGRESS
    
    # Tâche moyenne priorité
    task_id3 = manager.add_task(
        "Rédiger documentation technique",
        "Documentation complète de l'architecture",
        Priority.MEDIUM
    )
    task_ids.append(task_id3)
    
    # Tâche basse priorité
    task_id4 = manager.add_task(
        "Optimiser performances CSS",
        "Améliorer le temps de chargement des pages",
        Priority.LOW
    )
    task_ids.append(task_id4)
    
    # Tâche terminée
    task_id5 = manager.add_task(
        "Configurer environnement de test",
        "Mise en place de l'environnement de tests automatisés",
        Priority.MEDIUM
    )
    task_ids.append(task_id5)
    manager.get_task(task_id5).mark_completed()
    
    print(f"✓ {len(task_ids)} tâches de démonstration créées")
    print(f"  - 2 tâches terminées")
    print(f"  - 1 tâche en cours")
    print(f"  - 2 tâches en attente")
    print()
    
    # Créer le service d'export
    print("2. Création du service d'export...")
    export_service = ExportService()
    print(f"✓ Service d'export créé")
    print(f"  Formats supportés: {export_service.get_supported_formats()}")
    print()
    
    # Récupérer toutes les tâches
    tasks = list(manager)
    
    # Export JSON
    print("3. Export vers JSON...")
    try:
        success = export_service.export_tasks(
            tasks, 
            "export_demo_tasks.json", 
            "json", 
            include_statistics=True
        )
        if success:
            file_size = os.path.getsize("export_demo_tasks.json")
            print(f"✓ Export JSON réussi: export_demo_tasks.json ({file_size} octets)")
        else:
            print("✗ Échec de l'export JSON")
    except Exception as e:
        print(f"✗ Erreur lors de l'export JSON: {e}")
    print()
    
    # Export XML
    print("4. Export vers XML...")
    try:
        success = export_service.export_tasks(
            tasks, 
            "export_demo_tasks.xml", 
            "xml", 
            include_statistics=True
        )
        if success:
            file_size = os.path.getsize("export_demo_tasks.xml")
            print(f"✓ Export XML réussi: export_demo_tasks.xml ({file_size} octets)")
        else:
            print("✗ Échec de l'export XML")
    except Exception as e:
        print(f"✗ Erreur lors de l'export XML: {e}")
    print()
    
    # Export Excel
    print("5. Export vers Excel...")
    try:
        success = export_service.export_tasks(
            tasks, 
            "export_demo_tasks.xlsx", 
            "xlsx", 
            include_statistics=True
        )
        if success:
            file_size = os.path.getsize("export_demo_tasks.xlsx")
            print(f"✓ Export Excel réussi: export_demo_tasks.xlsx ({file_size} octets)")
            print("  - Feuille 'Tasks' avec toutes les tâches")
            print("  - Feuille 'Statistics' avec les statistiques")
        else:
            print("✗ Échec de l'export Excel")
    except ImportError as e:
        print(f"⚠ Dépendance manquante: {e}")
        print("  Installez openpyxl avec: pip install openpyxl")
    except Exception as e:
        print(f"✗ Erreur lors de l'export Excel: {e}")
    print()
    
    # Test d'export sans statistiques
    print("6. Export JSON sans statistiques...")
    try:
        success = export_service.export_tasks(
            tasks, 
            "export_demo_tasks_no_stats.json", 
            "json", 
            include_statistics=False
        )
        if success:
            file_size = os.path.getsize("export_demo_tasks_no_stats.json")
            print(f"✓ Export JSON sans statistiques réussi: export_demo_tasks_no_stats.json ({file_size} octets)")
        else:
            print("✗ Échec de l'export JSON sans statistiques")
    except Exception as e:
        print(f"✗ Erreur lors de l'export JSON sans statistiques: {e}")
    print()
    
    # Afficher l'historique des exports
    print("7. Historique des exports...")
    history = export_service.get_export_history()
    print(f"✓ {len(history)} export(s) effectué(s):")
    for i, export_info in enumerate(history, 1):
        status = "✓" if export_info.get("success", False) else "✗"
        print(f"  {i}. {status} {export_info['filename']} ({export_info['format'].upper()})")
        print(f"     - {export_info['task_count']} tâche(s)")
        print(f"     - Statistiques: {'Oui' if export_info['include_statistics'] else 'Non'}")
        print(f"     - Exporté le: {export_info['exported_at']}")
        if not export_info.get("success", False):
            print(f"     - Erreur: {export_info.get('error', 'Inconnue')}")
    print()
    
    # Résumé des fichiers créés
    print("8. Résumé des fichiers créés:")
    export_files = [
        "export_demo_tasks.json",
        "export_demo_tasks.xml", 
        "export_demo_tasks.xlsx",
        "export_demo_tasks_no_stats.json"
    ]
    
    for filename in export_files:
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({file_size} octets)")
        else:
            print(f"  ✗ {filename} (non créé)")
    
    print()
    print("9. Test des formats supportés...")
    test_formats = ['json', 'xml', 'xlsx', 'excel', 'csv', 'pdf']
    for format_type in test_formats:
        is_supported = export_service.is_format_supported(format_type)
        status = "✓" if is_supported else "✗"
        print(f"  {status} {format_type.upper()}: {'Supporté' if is_supported else 'Non supporté'}")
    
    print()
    print("=== Démonstration terminée ===")
    print()
    print("Pour ouvrir les fichiers exportés:")
    print("- JSON: cat export_demo_tasks.json")
    print("- XML: cat export_demo_tasks.xml")
    print("- Excel: libreoffice export_demo_tasks.xlsx")
    print()


if __name__ == "__main__":
    main() 