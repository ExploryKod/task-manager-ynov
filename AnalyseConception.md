# Phase 1 - Analyse et conception

Dans cette phase, j'ai définis mes entités (ou model) qui appartiennent au coeur le plus stable de l'application : ils ne changeront que trés peu. Ils forment le squelette de base et sont en lien direct avec le métier - ici un outil pour gérer ses tâches. 

Voici les fonctionnalités requises :
Créer, modifier, supprimer des tâches
Organiser les tâches par projet et priorité
Marquer les tâches comme terminées
Sauvegarder et charger depuis un fichier JSON
Générer des statistiques sur les tâches
Envoyer des notifications par email (simulé)

Questions d'analyse :
1. Quelles sont les entités principales ? (Tâche, Projet, Gestionnaire)
2. Quelles dépendances externes identifiez-vous ?
3. Quels cas d'erreur faut-il prévoir ?
4. Comment organiser le code pour faciliter les tests ?

## Les entités principales : 
- Des utilisateurs créer, supprimme, édite ou accède (CRUD) à un ou des projets
- Chaque projet est composé de tâches auxquels que chacun créer, supprimme, édite ou lis. Il est possible de leur donner un ordre de priorité et de les assigner à un ou plusieurs projets. Elles pourront être marqué comme "en cours" ou "terminées".
- Il y a plusieurs acteurs dans ce manager de tâche : un gestionnaire qui va contrôler les flux de tous les projets et tâches et un ou des utilisateurs qui auront certains droits sur leurs tâches et projets mais seulement les leurs.
- Une entité de notification se charge de prévenir par email les utilisateur et le manager de changements sur les tâches et projets.
- Une entité de reporting qui est chargé de créer des rapports quotidiens sur certains changements clés.

## Les dépendances externes du Task Manager

Voici les dépendances de notre application de gestion de tâches (au minimum): 
- Un service : un serveur email car il y a des notification par email (1)
- Un autre service : un système de stockage des rapports (2)
- Un espace où l'on persiste la donnée : base de donnée ou dans notre cas ce sera un simple système de fichiers json dans un premier temps.

(1) Dans notre cas nous allons simuler cette dépendance. Il existe aussi des outils comme mailtrap avec un tiers gratuit limité pour faire des tests plus réaliste sur de vrai serveur d'email.

(2) On pourrait utiliser des outils comme Amazon S3 ou cloudinary pour stocker des PDF par exemple mais dans notre cas on va en rester à nos système de fichiers json.

Il y a aussi des dépendances de type Devops :
- Un hébergement du code sur Github avec usage des Github Actions
- Un navigateur web pour faire fonctionner à minima localement 
- Un serveur pour que l'app (client) s'affiche sur un navigateur web

Voici des librairies et/ou framework desquels nous allons dépendre (au minimum) : 
- Un framework de test et ses outils connexes (ex: pytest)
- Un outil pour sérialiser/déserialiser le json
- Une librairie pour valider les données
- Une librairie pour gérer la protection de nos routes

Si l'on va plus loin avec des pages html nous aurons besoin d'un framework de type FastAPI ou Flask afin d'avoir des routes, afficher des templates en y mettant de la donnée dynamique, protéger des routes etc...

Le plus essentiel ici pour nos tests c'est que nous sachions d'un côté resté indépendant de l'appel des fichiers JSON ou de l'écriture de ces derniers en créant des mock mais aussi que nous veillons à bien isoler les erreurs API des autres erreurs et donc en validant l'entrée et la sortie des flux de donnée de notre app vers ces fichiers json. Ce serait la même préoccupation avec une base de donnée.

Nous devons aussi contrôler la sortie des emails/notification.

Les contrôles de rapports entiers peut se faire via des tests d'approbation ou "approval tests" à travers des outils comme les snapshots.

## Les cas d'erreurs à prévoir.

Il y a une série de cas d'erreurs à prévoir sur nos tests. 

1. Les tests sur les valeurs limites lié à la programmation :
- Calculs impossible comme division par zéro au moment de calculer des ratios pour nos rapports.
- Dépassement de valeurs maximales acceptable par nos fonctions (Ex: si l'on a limité à 100 tâches par projet, on teste la création de la 101ème tâche pour un projet).
- Les titres des tâches ou des projets sont limité en nombre maximal de caractère: tester les erreurs de dépassement 
- Les titres des tâches ou des projets sont limité en nombre minimal de caractère: tester les erreurs si pas assez de caractère
- Les titres des tâches et projets ne peuvent pas comporter certains caractères spéciaux et on doit éviter la faille XSS.
- Les slug de titres de projet et tâche ne doivent pas comporter d'espaces vide 

- Les collections de tâches ou de projets doivent avoir plus d'un élèment pour exister

- Tester la suppression d'une tâche ou un projet ayant un id null : cela doit engendrer une exception ou une erreur.

- La recherche d'une tâche ou d'un projet inexistant doit retourner un message à tester.

- les catégories de priorité doivent appartenir à des mots précis qui sont dans un type enum comme "URGENT".

- les statistiques ne se font pas sur les projets sans tâches qui sont des projets en attente (tout juste créé). Il faut au moins une tâche pour que les calculs se fassent.
- Fonctions de calculs: on test le taux de complétion des projets si toutes les tâches sont terminé : doit afficher 100%. On teste les cas limite en regardant si on a 101% comme résultat par exemple.

- La date doit respecter un format précis ISO et doit aussi être traduite correctement dans un format de type string le cas échéant.
- La date de création de projet/tâche doit être inférieur à la date d'édition (update_at) ou de suppression. 
- Les calculs de durée entre date ne doivent pas affiché des durées négatives impossible

Un email contient un "@" et une extension (.com, .fr ...)
Les emails sont limité en nombre de caractères
Les emails ne doivent pas avoir de caractères spéciaux non-autorisé

Nos système de fichiers JSON est limité à 150 fichiers JSON avec un nombre maximal de place mémoire : il faut tester les cas de dépassement et les exeptions.

Un échec de l'appel API de nos fichiers JSON : 
- Savoir si c'est la connexion internet qui ne marche pas
- Savoir si c'est l'addresse qui n'est pas la bonne (mauvais port, mauvaise addresse url ...)

Tester l'intégrité des fichiers JSON lors de la sérialisation (tester si un fichier est corrompu).

2. Des cas d'erreur limites lié au métier:
- Certaines tâches dépendande d'autres tâches : ne pas pouvoir les terminer avant la complémetion de toute les tâches ou vérifier que l'on propose à l'utilisateur un message d'alerte (ex: "Cette tâche a des tâches qui en dépendent, voulez-vous supprimer aussi les tâches dépendantes x ou y ?").
- Ne pas pouvoir supprimer un projet qui a encore des tâches non-terminé sans prévenir.
- Si une tâche A dépend d'une autre et que cette autre dépend de la tâche A: que se passe t-il ?
- Un export CSV ne peut se faire si il y a 0 tâche à exporter : vérfier cela en testant qu'un export sans tâche engendre un message d'exception et bloque le process.
- De même : tester qu'un rapport ne soit pas générer si il n'y a rien à rapporter (ex: 0 tâches)

A chaque cas ci-dessus on ne se contente pas de vérifier qu'il y a une erreur mais on va plus loin : on vérifie dans les cas où il y a une levée d'exception, le message explicit de l'exception pour avoir un retour trés précis. Soit on a créer ce message précis soit le système en fournit qui seront toujours les mêmes.

## Comment organiser le code pour faciliter les tests ?

1. Lisibilité et compréhension
- Respect d'un nommage cohérent qui décris bien le contexte du test : fonction/method testée suivi de la condition par exemple.
Exemple : test_get_tasks_with_low_priority
- Couplage faible entre les composants : notre architecture doit isoler ses use cases (ce qui fait sens niveau métier) afin de tester seulement des ensembles cohérents de dépendances et pouvoir découper ces ensemble aisément via des mock ou stub pour nos tests. Cela implique de bien organiser le code pour limiter les couplage fort entre composants.

- Chaque test aura une structure bien apparente basé sur le AAA (Arrange Act Assert) ou Given-When-Then. On prépare le test avec les données clairement puis on va tester le "system under test" (fonction, method, class ...) et enfin on va clairement obtenir un résultat (assert). Nous devons bien penser à y inclure toute information importante lors de la lecture des tests qui offrent alors aussi une documentation sur notre base de code.

- Les fichiers de tests doivent être un miroir des fichiers de l'application elle-même. Il reprennent le nommage et commence par "test_". 
- Le code doit clairement isoler et mettre en avant ses models ou entités qui sont le coeur du domaine métier (ex: Tasks, Project) afin que les tests s'appuient dessus aussi en créant des fixtures pour les reprendre par exemple.
- De même pour tout objet complexe qui sera repris dans des fixtures: cela permet d'être indépendant du code et ainsi testé plusieurs cas sans se répété dans nos tests (respect du DRY).
 


2. Maintenabilité 
- Chaque class représente une entité cohérente et chaque méthode a ses propes responsabilités limités. On respect le single responsibility principle (SRP) au mieux.
- Inversion de dépendance : permet de faire évoluer le code même si l'on dépend de la couche de persistance par exemple.
- Nos ensemble de tests sont isolés les uns des autres pour tester directement des morceaux de code eux-même bien séparé. On doit pouvoir tester sans dépendre d'autres morceaux de code si l'on veux.

