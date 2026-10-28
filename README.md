# Projet-MNAI — Environnement de simulation pour drone autonome

Ce dépôt Git est consacré au projet de **Méthodes Numériques pour l’Apprentissage Machine**.

L’objectif du projet est d’implémenter un environnement de simulation pour un **drone autonome de patrouille**. Le drone évolue dans une grille 2D discrète, possède une batterie limitée, doit éviter des zones dangereuses, revenir à sa base pour se recharger, et chercher à couvrir un maximum de zones de patrouille sans provoquer de crash.

Le projet met principalement l’accent sur la construction d’un environnement conforme à la spécification fournie. Cet environnement peut être utilisé par un agent humain via le mode interactif, par une séquence d’actions via le mode automatique, ou analysé avec une exploration exhaustive de l’espace d’états.

---

## Objectifs du projet

Le projet vise à modéliser :

- une grille 2D finie ;
- des zones de patrouille ;
- des cellules dangereuses ;
- l’état courant du drone ;
- les actions possibles du drone ;
- les transitions entre états ;
- les préconditions des actions ;
- les invariants de cohérence ;
- plusieurs modes d’exécution de l’environnement.

---

## Fonctionnalités principales

Le projet contient :

- une représentation d’une grille 2D discrète ;
- une gestion de zones de patrouille ;
- une gestion de cellules dangereuses ;
- un état complet du drone ;
- plusieurs actions du drone ;
- une vérification des invariants ;
- un mode de démonstration simple ;
- un mode interactif ;
- un mode automatique ;
- un mode exhaustif avec exploration DFS ;
- un fichier de tests de conformité ;
- plusieurs scénarios automatiques validés.

---

## Structure du projet

```text
Projet-MNAI/
│
├── Grille.py
├── EtatEnvironnement.py
├── DroneAgent.py
├── Simulation.py
├── main.py
│
├── mode_interactif.py
├── mode_automatique.py
├── mode_exhaustif.py
│
├── tests_conformite.py
├── scenario.csv
│
├── scenarios/
│   ├── scenario_basique.csv
│   ├── scenario_action_invalide.csv
│   ├── scenario_recharge.csv
│   ├── scenario_arret_urgence.csv
│   ├── scenario_retour_base.csv
│   └── scenario_patrouille_longue.csv
│
├── README.md
├── AVANCEMENT.md
└── VALIDATION_SCENARIOS.md
```

---

## Description des fichiers

### `Grille.py`

Ce fichier définit la grille 2D dans laquelle évolue le drone.

Il contient :

- `MaxX` et `MaxY` : les bornes de la grille ;
- `Danger` : l’ensemble des cellules dangereuses ;
- `ZoneCount` : le nombre de zones de patrouille ;
- `ZoneOf(x, y)` : la fonction qui retourne la zone d’une cellule ;
- `afficher()` : une méthode permettant d’afficher la grille.

Les cellules dangereuses sont représentées par le symbole `X`, le drone par le symbole `D`, et les autres cellules par `.`.

---

### `EtatEnvironnement.py`

Ce fichier représente l’état courant de l’environnement.

Il contient notamment :

- la position du drone : `posX`, `posY` ;
- la position de la base : `baseX`, `baseY` ;
- le niveau de batterie : `battery` ;
- la distance abstraite au danger : `obstacle_distance` ;
- l’état opérationnel du drone :
  - `docked` ;
  - `airborne` ;
  - `crashed` ;
- l’ensemble des zones visitées : `visZones`.

Il contient aussi plusieurs méthodes importantes :

- `check_invariant()` : vérifie la cohérence de l’état ;
- `get_state()` : retourne une représentation complète de l’état ;
- `is_terminal()` : indique si l’état courant est terminal ;
- `at_base()` : vérifie si le drone est à la base ;
- `all_zones_visited()` : vérifie si toutes les zones ont été visitées ;
- `mission_success()` : vérifie si la mission est réussie ;
- `voisins_valides()` : retourne les voisins accessibles ;
- `voisins_surs()` : retourne les voisins non dangereux ;
- `actions_possibles()` : retourne les actions autorisées ;
- `clone()` : crée une copie indépendante de l’environnement.

---

### `DroneAgent.py`

Ce fichier implémente les actions possibles du drone.

Actions disponibles :

- `takeoff_cmd()` : décollage du drone ;
- `move_step()` : déplacement élémentaire non déterministe ;
- `avoid_maneuver()` : déplacement d’évitement ;
- `return_home()` : retour vers la base ;
- `dock_cmd()` : arrimage à la base ;
- `undock_cmd()` : sortie de l’état docked ;
- `charge_step()` : recharge progressive ;
- `emergency_stop()` : arrêt d’urgence.

Chaque action vérifie ses préconditions avant de modifier l’état.

Si une précondition n’est pas respectée, l’action retourne `False`.

Si l’action est exécutée correctement, elle retourne `True`.

Après chaque action valide, les invariants de l’environnement sont vérifiés.

---

### `Simulation.py`

Ce fichier contient une classe `Simulation` qui centralise l’exécution des actions.

Elle permet d’exécuter une action à partir de son nom :

```python
simulation.execute_action("takeoff_cmd")
simulation.execute_action("move_step")
```

La méthode `execute_action(action)` vérifie d’abord que l’action appartient aux actions possibles dans l’état courant, puis appelle la méthode correspondante dans `DroneAgent`.

Ce fichier est utilisé par les modes interactif et automatique.

---

### `main.py`

Ce fichier sert de démonstration simple.

Il crée :

- une grille ;
- un environnement ;
- un agent ;

puis exécute quelques actions pour tester le comportement général du drone.

---

### `mode_interactif.py`

Ce fichier implémente le mode interactif.

Dans ce mode, l’utilisateur pilote manuellement le drone.

À chaque étape :

1. l’état courant est affiché ;
2. les actions possibles sont affichées ;
3. l’utilisateur choisit une action ;
4. l’environnement applique l’action ;
5. le nouvel état est affiché.

Le mode s’arrête lorsqu’un état terminal est atteint.

---

### `mode_automatique.py`

Ce fichier implémente le mode automatique.

Dans ce mode, le programme lit une séquence d’actions depuis un fichier CSV, puis exécute les actions dans l’ordre.

L’exécution s’arrête si :

- une action est invalide ;
- une précondition n’est pas satisfaite ;
- un état terminal est atteint.

Ce mode permet de rejouer des scénarios de test reproductibles.

Le mode automatique accepte aussi un fichier scénario et une seed aléatoire en arguments. Cela permet de reproduire les comportements non déterministes liés à `move_step()` et `avoid_maneuver()`.

---

### `mode_exhaustif.py`

Ce fichier implémente le mode exhaustif.

Ce mode explore récursivement les états atteignables depuis l’état initial à l’aide d’un parcours en profondeur, c’est-à-dire un DFS.

Il permet d’analyser :

- les états atteignables ;
- les transitions possibles ;
- les effets du non-déterminisme ;
- les états terminaux ;
- la couverture de l’espace d’états.

Les actions non déterministes comme `move_step()` et `avoid_maneuver()` sont traitées en générant tous les successeurs possibles au lieu d’en choisir un au hasard.

Le mode exhaustif affiche également :

- le nombre d’états atteignables ;
- le nombre de transitions ;
- quelques états visités ;
- quelques transitions sous la forme :
  - état source ;
  - action ;
  - état destination.

---

### `tests_conformite.py`

Ce fichier contient des tests permettant de vérifier la conformité de l’environnement.

Il teste notamment :

- l’état initial ;
- le décollage ;
- le déplacement ;
- la manœuvre d’évitement ;
- l’arrimage et la recharge ;
- l’arrêt d’urgence ;
- les actions invalides ;
- les situations de crash ;
- le retour à la base ;
- le maintien des invariants après les actions.

Ces tests permettent de vérifier que les principales opérations respectent les préconditions, les effets attendus et les invariants de l’environnement.

---

### `scenarios/`

Ce dossier contient plusieurs scénarios automatiques au format CSV.

Chaque fichier contient une séquence d’actions à exécuter.

Scénarios disponibles :

- `scenario_basique.csv` ;
- `scenario_action_invalide.csv` ;
- `scenario_recharge.csv` ;
- `scenario_arret_urgence.csv` ;
- `scenario_retour_base.csv` ;
- `scenario_patrouille_longue.csv`.

---

### `VALIDATION_SCENARIOS.md`

Ce fichier présente la validation des scénarios automatiques.

Il décrit :

- les scénarios testés ;
- la seed utilisée ;
- le résultat attendu ;
- le résultat observé ;
- le statut de validation.

---

## Lancer le projet

### 1. Démonstration simple

```bash
python3 main.py
```

Sous Windows :

```bash
python main.py
```

---

### 2. Mode interactif

```bash
python3 mode_interactif.py
```

Sous Windows :

```bash
python mode_interactif.py
```

Ce mode affiche l’état courant du drone et la liste des actions possibles.

Exemple d’affichage :

```text
Actions possibles :
0 - takeoff_cmd
1 - emergency_stop
```

L’utilisateur choisit une action en entrant son numéro.

---

### 3. Mode automatique

Commande simple :

```bash
python3 mode_automatique.py
```

Sous Windows :

```bash
python mode_automatique.py
```

Par défaut, le scénario est lu depuis :

```text
scenario.csv
```

Il est aussi possible de préciser le fichier scénario et la seed aléatoire :

```bash
python3 mode_automatique.py scenarios/scenario_basique.csv 0
```

Sous Windows :

```bash
python mode_automatique.py scenarios/scenario_basique.csv 0
```

Le second argument permet de fixer la seed utilisée pour les actions non déterministes. Cela rend les tests reproductibles.

---

### 4. Exemples de scénarios automatiques

```bash
python3 mode_automatique.py scenarios/scenario_basique.csv 0
python3 mode_automatique.py scenarios/scenario_action_invalide.csv 0
python3 mode_automatique.py scenarios/scenario_recharge.csv 0
python3 mode_automatique.py scenarios/scenario_arret_urgence.csv 0
python3 mode_automatique.py scenarios/scenario_retour_base.csv 0
python3 mode_automatique.py scenarios/scenario_patrouille_longue.csv 0
```

---

### 5. Mode exhaustif DFS

```bash
python3 mode_exhaustif.py
```

Sous Windows :

```bash
python mode_exhaustif.py
```

Ce mode affiche :

- la profondeur maximale utilisée ;
- la largeur maximale utilisée ;
- le nombre d’états atteignables ;
- le nombre de transitions ;
- quelques états visités ;
- quelques transitions.

---

### 6. Tests de conformité

```bash
python3 tests_conformite.py
```

Sous Windows :

```bash
python tests_conformite.py
```

Ces tests vérifient le bon comportement des principales opérations et le maintien des invariants.

---

## Représentation de l’état

Un état est représenté sous forme de tuple :

```python
(
    posX,
    posY,
    battery,
    obstacle_distance,
    docked,
    airborne,
    crashed,
    zones_visitees
)
```

Cette représentation est utilisée pour :

- comparer deux états ;
- éviter de revisiter plusieurs fois le même état ;
- explorer l’espace d’états.

---

## États terminaux

Un état est considéré comme terminal si :

- le drone est crashé ;
- la batterie est vide ;
- la mission est réussie.

Une mission est réussie lorsque :

- toutes les zones de patrouille ont été visitées ;
- le drone est revenu à la base ;
- le drone n’est pas crashé.

L’arrimage à la base est traité comme une opération supplémentaire permettant ensuite la recharge.

---

## Actions et préconditions

Chaque action possède des préconditions.

Par exemple, `move_step()` est possible seulement si :

- le drone n’est pas crashé ;
- le drone est en vol ;
- le drone n’est pas docked ;
- la batterie est strictement positive.

Si une précondition n’est pas respectée, l’action est refusée et l’état n’est pas modifié.

Les actions disponibles sont :

- `takeoff_cmd` ;
- `move_step` ;
- `avoid_maneuver` ;
- `return_home` ;
- `dock_cmd` ;
- `undock_cmd` ;
- `charge_step` ;
- `emergency_stop`.

---

## Invariants

Après chaque action valide, l’environnement vérifie ses invariants.

Les invariants garantissent notamment que :

- `posX` reste dans les limites de la grille ;
- `posY` reste dans les limites de la grille ;
- `battery` reste entre 0 et 100 ;
- `docked`, `airborne` et `crashed` valent toujours 0 ou 1 ;
- les zones visitées sont valides ;
- un drone crashé ne peut pas être en vol ;
- un drone arrimé ne peut pas être en vol ;
- un drone arrimé doit être à la base.

---

## Gestion du non-déterminisme

Certaines actions sont non déterministes.

C’est le cas de :

- `move_step()` ;
- `avoid_maneuver()`.

Dans le mode interactif et le mode automatique, ces actions choisissent un successeur possible de manière aléatoire.

Dans le mode exhaustif, elles sont traitées différemment : tous les successeurs possibles sont générés afin d’explorer correctement l’espace des états atteignables.

---

## Validation des scénarios

Les scénarios automatiques ont été testés avec la seed `0`.

Les résultats détaillés sont disponibles dans :

```text
VALIDATION_SCENARIOS.md
```

Tous les scénarios principaux sont validés :

- `scenario_basique.csv` ;
- `scenario_action_invalide.csv` ;
- `scenario_recharge.csv` ;
- `scenario_arret_urgence.csv` ;
- `scenario_retour_base.csv` ;
- `scenario_patrouille_longue.csv`.

---

## Avancement détaillé

Pour consulter l’historique détaillé de l’évolution du projet, voir le fichier :

```text
AVANCEMENT.md
```