# Avancement du projet MNAI

Ce document présente l’évolution du projet au fil des séances de travail.

Le projet consiste à implémenter un environnement de simulation pour un drone autonome de patrouille dans une grille 2D. L’objectif est de construire un environnement conforme à la spécification donnée, utilisable ensuite par un agent humain, un agent automatique ou un algorithme d’apprentissage par renforcement.

---

## DAY : 02/09/2026

### Initialisation du projet

Travail réalisé :

- création du dépôt Git ;
- première conception générale du projet ;
- début de l’implémentation de la classe `Grille` ;
- définition d’une grille simple ;
- ajout d’une première méthode d’affichage.

À ce stade, l’objectif était surtout de poser la base du projet et de commencer à représenter l’environnement dans lequel le drone évoluera.

Test possible :

```bash
python3 Grille.py
```

Sous Windows :

```bash
python Grille.py
```

---

## DAY : 03/23/2026

### Mise en place de l’architecture orientée objet

Travail réalisé :

- création de la classe `Grille` ;
- création de la classe `EtatEnvironnement` ;
- création de la classe `DroneAgent` ;
- ajout des premières variables d’état du drone ;
- ajout de la position du drone ;
- ajout de la batterie ;
- ajout des états opérationnels :
  - `docked` ;
  - `airborne` ;
  - `crashed` ;
- ajout de l’ensemble des zones visitées ;
- implémentation des premières actions :
  - `takeoff_cmd()` ;
  - `move_step()` ;
- création d’un premier fichier `main.py` pour tester la simulation ;
- ajout de l’affichage du drone dans la grille.

### Explication

Cette étape a permis de séparer les responsabilités entre plusieurs classes :

- `Grille` représente l’espace de déplacement ;
- `EtatEnvironnement` contient l’état courant du drone ;
- `DroneAgent` contient les actions que le drone peut exécuter.

Cette organisation rend le projet plus clair et facilite les évolutions futures.

Test possible :

```bash
python3 main.py
```

Sous Windows :

```bash
python main.py
```

---

## DAY : 04/02/2026

### Améliorations de conformité avec la spécification

Travail réalisé :

- correction des invariants ;
- remplacement de certains affichages d’erreurs par des `assert` pour mieux vérifier la cohérence de l’état ;
- amélioration de `move_step()` ;
- ajout d’un comportement non déterministe dans `move_step()` ;
- choix aléatoire d’un voisin valide ;
- correction de certains messages d’erreur ;
- suppression de mises à jour inutiles de `obstacle_distance` ;
- ajout de la gestion du danger ;
- crash automatique si le drone arrive sur une cellule dangereuse ;
- amélioration de la cohérence entre les états :
  - si le drone est crashé, il ne peut plus être en vol ;
  - si le drone est docked, il ne peut pas être airborne.

### Explication

Cette étape a rapproché le code de la spécification du sujet.

Les invariants servent à garantir que l’état de l’environnement reste toujours cohérent après chaque action.

Par exemple :

- une position ne doit pas sortir des limites de la grille ;
- la batterie doit rester entre 0 et 100 ;
- un drone crashé ne peut pas être en vol ;
- un drone docked doit être à la base.

---

## DAY : 04/26/2026

### Finalisation de l’environnement, des modes d’exécution et de la validation

Cette journée a permis de structurer l’environnement, d’ajouter les trois modes d’exécution demandés, de compléter les tests de conformité et de valider plusieurs scénarios automatiques.

---

### 1. Amélioration de `EtatEnvironnement.py`

Méthodes ajoutées :

- `get_state()` ;
- `is_terminal()` ;
- `at_base()` ;
- `all_zones_visited()` ;
- `mission_success()` ;
- `voisins_valides()` ;
- `voisins_surs()` ;
- `actions_possibles()` ;
- `clone()`.

#### `get_state()`

Retourne une représentation complète de l’état courant de l’environnement.

Cette méthode est utile pour :

- afficher l’état ;
- comparer deux états ;
- construire l’espace d’états ;
- préparer une utilisation avec un agent externe.

#### `is_terminal()`

Indique si l’état courant est terminal.

Un état est terminal si :

- le drone est crashé ;
- la batterie est vide ;
- la mission est réussie.

#### `at_base()`

Vérifie si le drone est actuellement à la base.

#### `all_zones_visited()`

Vérifie si toutes les zones de patrouille ont été visitées.

#### `mission_success()`

Vérifie si la mission est réussie.

La mission est réussie si :

- toutes les zones ont été visitées ;
- le drone est revenu à la base ;
- le drone n’est pas crashé.

#### `voisins_valides()`

Retourne les cellules voisines accessibles depuis la position courante, en respectant les limites de la grille.

#### `voisins_surs()`

Retourne les voisins valides qui ne sont pas dans l’ensemble `Danger`.

#### `actions_possibles()`

Retourne la liste des actions autorisées dans l’état courant.

Cette méthode centralise les préconditions des opérations.

Elle est utilisée dans :

- le mode interactif ;
- le mode automatique ;
- le mode exhaustif.

#### `clone()`

Crée une copie indépendante de l’environnement.

Cette méthode est nécessaire pour le mode exhaustif, car l’exploration DFS doit pouvoir tester plusieurs transitions sans modifier l’environnement original.

---

### 2. Amélioration de `DroneAgent.py`

Les actions du drone retournent maintenant `True` ou `False`.

Objectif :

- retourner `True` si l’action est exécutée correctement ;
- retourner `False` si une précondition n’est pas respectée ;
- permettre au mode automatique de s’arrêter proprement en cas d’action invalide.

Actions améliorées :

- `takeoff_cmd()` ;
- `move_step()` ;
- `avoid_maneuver()` ;
- `return_home()` ;
- `dock_cmd()` ;
- `undock_cmd()` ;
- `charge_step()` ;
- `emergency_stop()`.

### Explication

Avant cette amélioration, certaines actions affichaient seulement un message d’erreur lorsque leurs préconditions n’étaient pas respectées.

Maintenant, chaque action indique explicitement si elle a réussi ou échoué.

Cela facilite l’utilisation de l’environnement dans les différents modes d’exécution.

---

### 3. Ajout de `Simulation.py`

Création du fichier :

```text
Simulation.py
```

Ce fichier contient une classe `Simulation`.

Rôle :

- centraliser l’exécution des actions ;
- vérifier si une action est autorisée ;
- appeler la bonne méthode de `DroneAgent`.

Exemple d’utilisation :

```python
simulation.execute_action("takeoff_cmd")
simulation.execute_action("move_step")
```

### Explication

Cette classe évite de répéter le même code dans les modes interactif et automatique.

Au lieu d’écrire plusieurs conditions dans chaque fichier, on utilise une seule méthode :

```python
execute_action(action)
```

---

### 4. Ajout du mode interactif

Création du fichier :

```text
mode_interactif.py
```

Fonctionnement :

- affiche l’état courant ;
- affiche les actions possibles ;
- demande à l’utilisateur de choisir une action ;
- exécute l’action choisie ;
- affiche le nouvel état ;
- s’arrête si un état terminal est atteint.

Commande :

```bash
python3 mode_interactif.py
```

Sous Windows :

```bash
python mode_interactif.py
```

### Explication

Ce mode permet de piloter le drone manuellement et de vérifier facilement l’effet de chaque action sur l’environnement.

---

### 5. Ajout du mode automatique

Création du fichier :

```text
mode_automatique.py
```

Fonctionnement :

- lit une séquence d’actions depuis un fichier CSV ;
- exécute les actions une par une ;
- affiche l’état après chaque action ;
- s’arrête si une action est invalide ;
- s’arrête si un état terminal est atteint ;
- permet de fixer une seed aléatoire pour rendre les scénarios reproductibles.

Commande avec scénario et seed :

```bash
python3 mode_automatique.py scenarios/scenario_basique.csv 0
```

### Explication

Ce mode permet de rejouer des scénarios automatiques et de vérifier le comportement du drone sans intervention manuelle.

---

### 6. Ajout du mode exhaustif DFS

Création du fichier :

```text
mode_exhaustif.py
```

Fonctionnement :

- part de l’état initial ;
- explore récursivement les états atteignables ;
- utilise une exploration en profondeur, ou DFS ;
- évite de revisiter les états déjà rencontrés ;
- prend en compte le non-déterminisme de certaines actions ;
- stocke les transitions explorées.

Actions non déterministes traitées :

- `move_step()` ;
- `avoid_maneuver()`.

Résultat observé avec `maxDepth = 10` :

```text
Nombre d'états atteignables : 774
Nombre de transitions : 2240
```

### Explication

Dans le mode interactif ou automatique, `move_step()` choisit un voisin aléatoirement.

Dans le mode exhaustif, on ne choisit pas un seul voisin au hasard. Tous les successeurs possibles sont générés afin d’explorer correctement l’espace des états atteignables.

---

### 7. Ajout des tests de conformité

Création du fichier :

```text
tests_conformite.py
```

Tests ajoutés :

- tests de l’état initial ;
- tests du décollage ;
- tests du déplacement ;
- tests de la manœuvre d’évitement ;
- tests de l’arrimage et de la recharge ;
- tests de l’arrêt d’urgence ;
- tests des actions invalides ;
- tests des situations de crash ;
- tests du retour à la base.

Commande :

```bash
python3 tests_conformite.py
```

Résultat obtenu :

```text
Tous les tests de conformité sont passés.
```

---

### 8. Ajout des scénarios automatiques

Ajout d’un dossier :

```text
scenarios/
```

Scénarios ajoutés :

- `scenario_basique.csv` ;
- `scenario_action_invalide.csv` ;
- `scenario_recharge.csv` ;
- `scenario_arret_urgence.csv` ;
- `scenario_retour_base.csv` ;
- `scenario_patrouille_longue.csv`.

Les scénarios ont été testés avec la seed `0`.

Tous les scénarios principaux ont produit le comportement attendu.

Les détails de validation sont disponibles dans :

```text
VALIDATION_SCENARIOS.md
```

---

### 9. Mise à jour de la documentation du dépôt

Fichiers de documentation ajoutés ou mis à jour :

- `README.md` ;
- `AVANCEMENT.md` ;
- `VALIDATION_SCENARIOS.md`.

Le `README.md` présente le projet, les fichiers principaux et les commandes d’exécution.

Le fichier `AVANCEMENT.md` présente l’évolution du travail.

Le fichier `VALIDATION_SCENARIOS.md` présente les résultats des scénarios automatiques.

---

## État actuel du projet

Le projet contient maintenant :

- un environnement de grille ;
- un état du drone cohérent avec la spécification ;
- les actions principales du drone ;
- une vérification des invariants ;
- un mode de démonstration simple ;
- un mode interactif ;
- un mode automatique ;
- un mode exhaustif DFS ;
- un affichage des transitions dans le mode exhaustif ;
- un fichier de tests de conformité ;
- des tests pour les actions invalides ;
- des tests pour les situations de crash ;
- des tests pour le retour à la base ;
- plusieurs scénarios automatiques validés.

---

## Commandes utiles

### Lancer la démonstration simple

```bash
python3 main.py
```

### Lancer le mode interactif

```bash
python3 mode_interactif.py
```

### Lancer le mode automatique avec le scénario par défaut

```bash
python3 mode_automatique.py
```

### Lancer un scénario automatique précis avec seed

```bash
python3 mode_automatique.py scenarios/scenario_basique.csv 0
```

### Lancer le mode exhaustif

```bash
python3 mode_exhaustif.py
```

### Lancer les tests de conformité

```bash
python3 tests_conformite.py
```

---

## Résumé de l’avancement

| Date       | Travail principal               |
|------------|---------------------------------------|
| 02/09/2026 | Initialisation du projet et début de `Grille.py` |
| 03/23/2026 | Architecture orientée objet et premières actions |
| 04/02/2026 | Invariants, non-déterminisme, gestion du danger |
|            | Modes interactif, automatique, exhaustif DFS, tests et scénarios |

---

## Conclusion temporaire

À ce stade, le projet possède une base fonctionnelle et structurée.

L’environnement respecte les principales contraintes de la spécification :

- état du drone ;
- batterie ;
- zones visitées ;
- cellules dangereuses ;
- préconditions des actions ;
- invariants ;
- actions métier ;
- modes d’utilisation ;
- exploration des états atteignables ;
- tests de conformité ;
- scénarios automatiques reproductibles.