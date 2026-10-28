# Validation des scénarios automatiques

Ce document présente les tests réalisés sur les scénarios automatiques du projet.

Les scénarios ont été exécutés avec une seed aléatoire fixée à `0` afin de rendre les comportements non déterministes reproductibles.

---

## Objectif

L’objectif de cette validation est de vérifier que le mode automatique :

- lit correctement un fichier de scénario au format CSV ;
- exécute les actions dans l’ordre ;
- respecte les préconditions des actions ;
- s’arrête si une action est invalide ;
- s’arrête si un état terminal est atteint ;
- maintient un état cohérent de l’environnement ;
- gère correctement les actions non déterministes grâce à une seed fixée.

---

## Commande générale utilisée

La commande utilisée pour lancer un scénario est :

```bash
python3 mode_automatique.py scenarios/nom_du_scenario.csv 0
```

Exemple :

```bash
python3 mode_automatique.py scenarios/scenario_basique.csv 0
```

Le dernier argument correspond à la seed aléatoire.

---

## Résumé des scénarios testés

| Scénario | Seed | Résultat attendu | Résultat observé | Statut |
|---|---:|---|---|---|
| `scenario_basique.csv` | 0 | Scénario simple avec retour puis arrimage | Exécution complète, retour à la base, arrimage et recharge effectués | OK |
| `scenario_action_invalide.csv` | 0 | Refus de `move_step` avant décollage | Action refusée, arrêt du scénario | OK |
| `scenario_recharge.csv` | 0 | Décollage, arrimage, recharge, undock, déplacement | Scénario exécuté correctement | OK |
| `scenario_arret_urgence.csv` | 0 | Arrêt après `emergency_stop` | État terminal atteint, arrêt du scénario | OK |
| `scenario_retour_base.csv` | 0 | Déplacement, retour base, arrimage, recharge | Scénario exécuté correctement | OK |
| `scenario_patrouille_longue.csv` | 0 | Exploration, évitement, retour, recharge, reprise | Scénario exécuté correctement | OK |

---

## Détail des validations

### `scenario_basique.csv`

Ce scénario teste une séquence simple comprenant :

- un décollage ;
- plusieurs déplacements ;
- une manœuvre d’évitement ;
- un retour à la base ;
- un arrimage ;
- une recharge.

Résultat observé :

- le drone décolle correctement ;
- les déplacements modifient la position et consomment de la batterie ;
- `avoid_maneuver` consomme 2 unités de batterie ;
- `return_home` rapproche le drone de la base ;
- une fois à la base, `dock_cmd` est accepté ;
- `charge_step` augmente la batterie.

Validation : OK.

---

### `scenario_action_invalide.csv`

Ce scénario commence par `move_step` alors que le drone n’a pas encore décollé.

Résultat attendu :

- `move_step` doit être refusée ;
- le scénario doit s’arrêter ;
- l’état doit rester cohérent.

Résultat observé :

- `move_step` est refusée ;
- le message `Action non autorisée : move_step` est affiché ;
- le scénario s’arrête immédiatement.

Validation : OK.

---

### `scenario_recharge.csv`

Ce scénario teste l’arrimage et la recharge.

Séquence testée :

- `takeoff_cmd` ;
- `dock_cmd` ;
- `charge_step` ;
- `charge_step` ;
- `undock_cmd` ;
- `move_step`.

Résultat observé :

- le drone décolle ;
- le drone s’arrime à la base ;
- `charge_step` est accepté ;
- `undock_cmd` est accepté ;
- le drone peut ensuite se déplacer.

Validation : OK.

---

### `scenario_arret_urgence.csv`

Ce scénario teste l’arrêt d’urgence.

Séquence testée :

- `takeoff_cmd` ;
- `move_step` ;
- `emergency_stop` ;
- `move_step`.

Résultat attendu :

- `emergency_stop` doit placer le drone dans un état de crash ;
- l’état doit devenir terminal ;
- les actions suivantes ne doivent pas être exécutées.

Résultat observé :

- `crashed` passe à `1` ;
- `airborne` passe à `0` ;
- `obstacle_distance` passe à `0` ;
- l’état terminal est détecté ;
- le dernier `move_step` n’est pas exécuté.

Validation : OK.

---

### `scenario_retour_base.csv`

Ce scénario teste le retour à la base.

Séquence testée :

- `takeoff_cmd` ;
- `move_step` ;
- `return_home` ;
- `dock_cmd` ;
- `charge_step`.

Résultat observé avec la seed `0` :

- le drone décolle ;
- le drone se déplace en `(1, 0)` ;
- `return_home` le ramène à la base `(0, 0)` ;
- `dock_cmd` est accepté ;
- `charge_step` recharge la batterie.

Validation : OK.

---

### `scenario_patrouille_longue.csv`

Ce scénario teste un comportement plus complet.

Il combine :

- exploration ;
- déplacement ;
- manœuvre d’évitement ;
- retour à la base ;
- arrimage ;
- recharge ;
- redécollage ;
- reprise de patrouille.

Résultat observé :

- le drone explore plusieurs cellules ;
- `avoid_maneuver` est exécutée ;
- la batterie diminue correctement ;
- les zones visitées évoluent ;
- le drone revient à la base ;
- il s’arrime ;
- il recharge ;
- il repart avec `undock_cmd` ;
- il peut continuer la patrouille.

Validation : OK.

---

## Remarques sur le non-déterminisme

Les actions suivantes sont non déterministes :

- `move_step()` ;
- `avoid_maneuver()`.

Cela signifie que plusieurs états suivants sont possibles.

Dans le mode automatique, un seul successeur est choisi aléatoirement. Pour rendre les tests reproductibles, une seed est utilisée.

Dans cette validation, la seed utilisée est :

```text
0
```

Grâce à cette seed, les résultats observés peuvent être reproduits.

---

## Conclusion

La validation des scénarios automatiques montre que l’environnement respecte les comportements attendus.

Les scénarios permettent de vérifier :

- les actions valides ;
- les actions invalides ;
- l’arrêt en cas d’état terminal ;
- le retour à la base ;
- l’arrimage ;
- la recharge ;
- la reprise de mission ;
- le bon fonctionnement du mode automatique.

Tous les scénarios testés avec la seed `0` sont validés.