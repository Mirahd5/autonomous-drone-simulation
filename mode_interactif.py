from Grille import Grille
from EtatEnvironnement import EtatEnvironnement
from DroneAgent import DroneAgent
from Simulation import Simulation


def afficher_etat(env):
    print("\n--- ETAT COURANT ---")
    env.afficher()
    print("Position :", env.posX, env.posY)
    print("Batterie :", env.battery)
    print("Airborne :", env.airborne)
    print("Docked :", env.docked)
    print("Crashed :", env.crashed)
    print("Zones visitées :", env.visZones)
    print("Etat terminal :", env.is_terminal())


def mode_interactif():
    grille = Grille(5, 5)
    env = EtatEnvironnement(grille)
    agent = DroneAgent(env)
    simulation = Simulation(env, agent)

    print("=== MODE INTERACTIF ===")

    while not env.is_terminal():
        afficher_etat(env)

        actions = env.actions_possibles()

        print("\nActions possibles :")
        for i, action in enumerate(actions):
            print(i, "-", action)

        choix = input("Choisir une action : ")

        try:
            indice = int(choix)

            if indice < 0 or indice >= len(actions):
                print("Choix invalide.")
                continue

            action = actions[indice]

        except ValueError:
            print("Choix invalide : veuillez entrer un nombre.")
            continue

        success = simulation.execute_action(action)

        if not success:
            print("Action refusée.")

    print("\n=== FIN DE L'EPISODE ===")
    afficher_etat(env)


if __name__ == "__main__":
    mode_interactif()