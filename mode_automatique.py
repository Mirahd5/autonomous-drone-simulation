import csv
import sys
import random

from Grille import Grille
from EtatEnvironnement import EtatEnvironnement
from DroneAgent import DroneAgent
from Simulation import Simulation


def lire_scenario(fichier):
    actions = []

    try:
        with open(fichier, "r") as f:
            reader = csv.reader(f)

            for ligne in reader:
                if len(ligne) == 0:
                    continue

                action = ligne[0].strip()

                if action != "":
                    actions.append(action)

    except FileNotFoundError:
        print("Fichier scénario introuvable :", fichier)

    return actions


def afficher_etat(env):
    env.afficher()
    print("Position :", env.posX, env.posY)
    print("Batterie :", env.battery)
    print("Airborne :", env.airborne)
    print("Docked :", env.docked)
    print("Crashed :", env.crashed)
    print("Obstacle distance :", env.obstacle_distance)
    print("Zones visitées :", env.visZones)
    print("Actions possibles :", env.actions_possibles())
    print()


def mode_automatique(fichier, seed=0):
    random.seed(seed)

    grille = Grille(5, 5)
    env = EtatEnvironnement(grille)
    agent = DroneAgent(env)
    simulation = Simulation(env, agent)

    actions = lire_scenario(fichier)

    if len(actions) == 0:
        print("Aucune action à exécuter.")
        return

    print("=== MODE AUTOMATIQUE ===")
    print("Fichier scénario :", fichier)
    print("Seed aléatoire :", seed)
    afficher_etat(env)

    for action in actions:
        if env.is_terminal():
            print("Etat terminal atteint. Arrêt du scénario.")
            break

        print("Action :", action)

        success = simulation.execute_action(action)

        if not success:
            print("Action invalide. Arrêt du scénario.")
            break

        afficher_etat(env)

    print("=== FIN DU MODE AUTOMATIQUE ===")


if __name__ == "__main__":
    fichier = "scenario.csv"
    seed = 0

    if len(sys.argv) >= 2:
        fichier = sys.argv[1]

    if len(sys.argv) >= 3:
        seed = int(sys.argv[2])

    mode_automatique(fichier, seed)