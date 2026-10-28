from EtatEnvironnement import EtatEnvironnement
from DroneAgent import DroneAgent
from Grille import Grille


def main():
    # Création de la grille 5x5
    g = Grille(5, 5)

    # Création de l'environnement
    env = EtatEnvironnement(g)

    # Création de l'agent qui agit sur cet environnement
    agent = DroneAgent(env)

    print("=== ETAT INITIAL ===")
    env.afficher()
    print("Position :", env.posX, env.posY)
    print("Batterie :", env.battery)
    print("Zones visitées :", env.visZones)
    print("Crash :", env.crashed)

    print("\n=== DECOLLAGE ===")
    agent.takeoff_cmd()
    env.afficher()

    print("\n=== MOVE 1 ===")
    agent.move_step()
    env.afficher()

    print("\n=== MOVE 2 ===")
    agent.move_step()
    env.afficher()

    print("\n=== AVOID MANEUVER ===")
    agent.avoid_maneuver()
    env.afficher()

    print("\n=== ETAT FINAL ===")
    print("Position :", env.posX, env.posY)
    print("Batterie :", env.battery)
    print("Zones visitées :", env.visZones)
    print("Obstacle distance :", env.obstacle_distance)
    print("Crash :", env.crashed)
    print("Airborne :", env.airborne)
    print("Docked :", env.docked)


if __name__ == "__main__":
    main()