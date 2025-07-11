#!/usr/bin/env python3
"""
Exemple simple d'utilisation de la fonctionnalité d'export
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status

def main():
    print("=== Exemple d'export TaskManager ===\n")
    
    # 1. Créer un gestionnaire avec des tâches
    print("1. Création de tâches d'exemple...")
    manager = TaskManager("demo_task_reports/json/example_tasks.json")
    
    # Ajouter quelques tâches
    manager.add_task("Développer nouvelle fonctionnalité", "Implémenter l'export multi-format", Priority.HIGH)
    manager.add_task("Corriger bugs", "Résoudre les issues remontées", Priority.URGENT)
    manager.add_task("Mettre à jour documentation", "Documenter les nouvelles fonctionnalités", Priority.MEDIUM)
    
    # Marquer une tâche comme terminée
    task = list(manager)[0]
    task.mark_completed()
    
    print(f"✓ {len(manager)} tâches créées")
    print(f"  - 1 tâche terminée")
    print(f"  - {len(manager) - 1} tâches en cours")
    
    # 2. Exporter vers différents formats
    print("\n2. Export vers différents formats...")
    
    # Export JSON avec statistiques
    try:
        success = manager.export_tasks("demo_task_reports/json/rapport_tasks.json", "json", include_statistics=True)
        print(f"✓ Export JSON: {'Réussi' if success else 'Échoué'}")
    except Exception as e:
        print(f"✗ Export JSON: Erreur - {e}")
    
    # Export XML avec statistiques
    try:
        success = manager.export_tasks("demo_task_reports/xml/rapport_tasks.xml", "xml", include_statistics=True)
        print(f"✓ Export XML: {'Réussi' if success else 'Échoué'}")
    except Exception as e:
        print(f"✗ Export XML: Erreur - {e}")
    
    # Export Excel avec statistiques
    try:
        success = manager.export_tasks("demo_task_reports/xlsx/rapport_tasks.xlsx", "xlsx", include_statistics=True)
        print(f"✓ Export Excel: {'Réussi' if success else 'Échoué'}")
    except Exception as e:
        print(f"✗ Export Excel: Erreur - {e}")
    
    # 3. Afficher les formats supportés
    print("\n3. Formats supportés:")
    formats = manager.get_export_formats()
    for fmt in formats:
        print(f"  - {fmt.upper()}")
    
    print("\n=== Exemple terminé ===")
    print("Fichiers créés:")
    print("  - demo_task_reports/json/rapport_tasks.json (JSON avec statistiques)")
    print("  - demo_task_reports/xml/rapport_tasks.xml (XML avec statistiques)")
    print("  - demo_task_reports/xlsx/rapport_tasks.xlsx (Excel avec onglets Tasks et Statistics)")
    print("\nStructure des dossiers:")
    print("  demo_task_reports/")
    print("  ├── json/    (Rapports JSON)")
    print("  ├── xml/     (Rapports XML)")
    print("  └── xlsx/    (Rapports Excel)")

if __name__ == "__main__":
    main() 