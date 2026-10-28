from Grille import Grille
from EtatEnvironnement import EtatEnvironnement

def mode_exhaustif():
    grille = Grille(5, 5)
    env = EtatEnvironnement(grille)

    visited = set()
    transitions_graph = []

    maxDepth = 10
    maxBreadth = -1

    explore(env, visited, transitions_graph, maxDepth, maxBreadth)

    print("=== MODE EXHAUSTIF DFS ===")
    print("Profondeur maximale :", maxDepth)
    print("Largeur maximale :", maxBreadth)
    print("Nombre d'états atteignables :", len(visited))
    print("Nombre de transitions :", len(transitions_graph))

    print("\nQuelques états visités :")
    for i, state in enumerate(visited):
        if i >= 10:
            break
        print(state)

    print("\nQuelques transitions :")
    for i, transition in enumerate(transitions_graph):
        if i >= 10:
            break

        source, action, destination = transition
        print("SOURCE :", source)
        print("ACTION :", action)
        print("DESTINATION :", destination)
        print()
        
def appliquer_deplacement(env, nextX, nextY, cout_batterie):
    """
    Applique un déplacement vers une case donnée.
    Cette fonction est utilisée pour générer les successeurs en DFS.
    """
    new_env = env.clone()

    new_env.posX = nextX
    new_env.posY = nextY
    new_env.battery -= cout_batterie
    new_env.visZones.add(new_env.get_zone(nextX, nextY))

    new_env.update_obstacle_distance()
    new_env.check_invariant()

    return new_env


def successeurs(env):
    """
    Génère toutes les transitions possibles depuis l'état courant.

    Chaque transition est représentée par :
    (nom_action, nouvel_environnement)
    """
    transitions = []

    if env.is_terminal():
        return transitions

    actions = env.actions_possibles()

    for action in actions:

        if action == "takeoff_cmd":
            new_env = env.clone()
            new_env.airborne = 1
            new_env.docked = 0
            new_env.update_obstacle_distance()
            new_env.check_invariant()
            transitions.append((action, new_env))

        elif action == "move_step":
            for (x, y) in env.voisins_valides():
                new_env = appliquer_deplacement(env, x, y, 1)
                transitions.append((action + f" -> ({x},{y})", new_env))

        elif action == "avoid_maneuver":
            voisins_surs = env.voisins_surs()

            if len(voisins_surs) > 0:
                for (x, y) in voisins_surs:
                    new_env = appliquer_deplacement(env, x, y, 2)
                    transitions.append((action + f" -> ({x},{y})", new_env))
            else:
                for (x, y) in env.voisins_valides():
                    new_env = appliquer_deplacement(env, x, y, 2)
                    transitions.append((action + f" -> ({x},{y})", new_env))

        elif action == "return_home":
            new_env = env.clone()

            if new_env.posX < new_env.baseX:
                nextX = new_env.posX + 1
            elif new_env.posX > new_env.baseX:
                nextX = new_env.posX - 1
            else:
                nextX = new_env.posX

            if new_env.posY < new_env.baseY:
                nextY = new_env.posY + 1
            elif new_env.posY > new_env.baseY:
                nextY = new_env.posY - 1
            else:
                nextY = new_env.posY

            new_env = appliquer_deplacement(env, nextX, nextY, 1)
            transitions.append((action, new_env))

        elif action == "dock_cmd":
            new_env = env.clone()
            new_env.docked = 1
            new_env.airborne = 0
            new_env.check_invariant()
            transitions.append((action, new_env))

        elif action == "undock_cmd":
            new_env = env.clone()
            new_env.docked = 0
            new_env.airborne = 1
            new_env.visZones.add(new_env.get_zone(new_env.posX, new_env.posY))
            new_env.check_invariant()
            transitions.append((action, new_env))

        elif action == "charge_step":
            new_env = env.clone()

            if new_env.battery <= 95:
                new_env.battery += 5
            else:
                new_env.battery = 100

            new_env.check_invariant()
            transitions.append((action, new_env))

        elif action == "emergency_stop":
            new_env = env.clone()
            new_env.crashed = 1
            new_env.airborne = 0
            new_env.docked = 0
            new_env.obstacle_distance = 0
            new_env.check_invariant()
            transitions.append((action, new_env))

    return transitions


def explore(env, visited, transitions_graph, maxDepth=-1, maxBreadth=-1):
    """
    Exploration DFS des états atteignables.

    visited contient les états déjà visités.
    transitions_graph contient les transitions :
    (etat_source, action, etat_destination)
    """
    state = env.get_state()

    if state in visited:
        return

    visited.add(state)

    if maxDepth != -1 and maxDepth <= 0:
        return

    count = 0

    for action, next_env in successeurs(env):
        if maxBreadth != -1 and count >= maxBreadth:
            break

        next_state = next_env.get_state()

        transitions_graph.append((state, action, next_state))

        if maxDepth == -1:
            next_depth = -1
        else:
            next_depth = maxDepth - 1

        explore(next_env, visited, transitions_graph, next_depth, maxBreadth)

        count += 1

if __name__ == "__main__":
    mode_exhaustif()