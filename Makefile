install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

coverage:
	pytest --cov=src --cov-report=html

clean:
	rm -rf .pytest_cache htmlcov __pycache__
	find . -type f -name '*.pyc' -delete

lint:
	@echo "Vérification de la syntaxe Python..."
	@files=$$(find src/ -name '*.py'); \
	if [ -z "$$files" ]; then \
		echo "Aucun fichier Python trouvé dans src/"; \
	else \
		echo "Fichiers à vérifier:"; \
		for file in $$files; do \
			echo "  - $$file"; \
		done; \
		echo ""; \
		echo "Compilation des fichiers..."; \
		for file in $$files; do \
			if python -m py_compile "$$file" 2>/dev/null; then \
				echo "✓ $$file"; \
			else \
				echo "✗ $$file - ERREUR DE SYNTAXE"; \
				python -m py_compile "$$file"; \
			fi; \
		done; \
		echo ""; \
		echo "Vérification terminée."; \
	fi

open-coverage-current:
	@echo "Ouverture du rapport de couverture actuel..."
	@if [ -f htmlcov/index.html ]; then \
		if command -v xdg-open > /dev/null 2>&1; then \
			xdg-open htmlcov/index.html; \
		elif command -v open > /dev/null 2>&1; then \
			open htmlcov/index.html; \
		elif command -v start > /dev/null 2>&1; then \
			start htmlcov/index.html; \
		else \
			echo "Impossible d'ouvrir le fichier. Ouvrez manuellement: htmlcov/index.html"; \
		fi; \
	else \
		echo "Aucun rapport de couverture actuel trouvé. Lancez 'make coverage' d'abord."; \
	fi

open-coverage-first:
	@echo "Ouverture du premier rapport de couverture (couverture insuffisante)..."
	@if [ -f rapports_couvertures/premier/htmlcov/index.html ]; then \
		if command -v xdg-open > /dev/null 2>&1; then \
			xdg-open rapports_couvertures/premier/htmlcov/index.html; \
		elif command -v open > /dev/null 2>&1; then \
			open rapports_couvertures/premier/htmlcov/index.html; \
		elif command -v start > /dev/null 2>&1; then \
			start rapports_couvertures/premier/htmlcov/index.html; \
		else \
			echo "Impossible d'ouvrir le fichier. Ouvrez manuellement: rapports_couvertures/premier/htmlcov/index.html"; \
		fi; \
	else \
		echo "Rapport de couverture 'premier' introuvable: rapports_couvertures/premier/htmlcov/index.html"; \
	fi

open-coverage-final:
	@echo "Ouverture du rapport de couverture final (95%)..."
	@if [ -f rapports_couvertures/couverture_95percent/htmlcov/index.html ]; then \
		if command -v xdg-open > /dev/null 2>&1; then \
			xdg-open rapports_couvertures/couverture_95percent/htmlcov/index.html; \
		elif command -v open > /dev/null 2>&1; then \
			open rapports_couvertures/couverture_95percent/htmlcov/index.html; \
		elif command -v start > /dev/null 2>&1; then \
			start rapports_couvertures/couverture_95percent/htmlcov/index.html; \
		else \
			echo "Impossible d'ouvrir le fichier. Ouvrez manuellement: rapports_couvertures/couverture_95percent/htmlcov/index.html"; \
		fi; \
	else \
		echo "Rapport de couverture 'final' introuvable: rapports_couvertures/couverture_95percent/htmlcov/index.html"; \
	fi

demo-export:
	python demo_export_simple.py

run-demo-export: demo-export

help:
	@echo "Commandes disponibles:"
	@echo "  install              - Installer les dépendances"
	@echo "  test                 - Lancer tous les tests"
	@echo "  test-unit            - Lancer les tests unitaires"
	@echo "  test-integration     - Lancer les tests d'intégration"
	@echo "  coverage             - Générer le rapport de couverture"
	@echo "  demo-export          - Démonstration de l'export multi-format"
	@echo "  open-coverage-current - Ouvrir le rapport de couverture actuel"
	@echo "  open-coverage-first  - Ouvrir le premier rapport (couverture insuffisante)"
	@echo "  open-coverage-final  - Ouvrir le rapport final (95%)"
	@echo "  clean                - Nettoyer les fichiers temporaires"
	@echo "  lint                 - Vérifier la syntaxe Python"
	@echo "  all                  - Exécuter clean, install, lint, test et coverage"

all: clean install lint test coverage 