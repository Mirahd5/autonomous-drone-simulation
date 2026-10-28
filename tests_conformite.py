from Grille import Grille
from EtatEnvironnement import EtatEnvironnement
import DroneAgent as drone_module


def create_env_agent():
    """
    Fonction utilitaire pour éviter de répéter la création
    de la grille, de l'environnement et de l'agent dans chaque test.
    """
    g = Grille(5, 5)
    env = EtatEnvironnement(g)
    agent = drone_module.DroneAgent(env)
    return g, env, agent


# ============================================================
# TESTS DE BASE
# ============================================================

def test_initialisation():
    g, env, agent = create_env_agent()

    assert env.posX == 0
    assert env.posY == 0
    assert env.baseX == 0
    assert env.baseY == 0
    assert env.battery == 100
    assert env.docked == 0
    assert env.airborne == 0
    assert env.crashed == 0
    assert env.obstacle_distance == 2
    assert env.visZones == {1}

    env.check_invariant()
    print("test_initialisation OK")


def test_takeoff():
    g, env, agent = create_env_agent()

    assert agent.takeoff_cmd() == True
    assert env.airborne == 1
    assert env.docked == 0
    assert env.crashed == 0

    env.check_invariant()
    print("test_takeoff OK")


def test_move_step():
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    old_battery = env.battery
    old_position = (env.posX, env.posY)

    assert agent.move_step() == True
    assert env.battery == old_battery - 1
    assert (env.posX, env.posY) != old_position

    env.check_invariant()
    print("test_move_step OK")


def test_avoid_maneuver():
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    old_battery = env.battery
    old_position = (env.posX, env.posY)

    assert agent.avoid_maneuver() == True
    assert env.battery == old_battery - 2
    assert (env.posX, env.posY) != old_position

    env.check_invariant()
    print("test_avoid_maneuver OK")


def test_dock_charge():
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    assert agent.dock_cmd() == True
    assert env.docked == 1
    assert env.airborne == 0

    env.battery = 90

    assert agent.charge_step() == True
    assert env.battery == 95

    env.check_invariant()
    print("test_dock_charge OK")


def test_emergency_stop():
    g, env, agent = create_env_agent()

    assert agent.emergency_stop() == True

    assert env.crashed == 1
    assert env.airborne == 0
    assert env.docked == 0
    assert env.obstacle_distance == 0
    assert env.is_terminal() == True

    env.check_invariant()
    print("test_emergency_stop OK")


# ============================================================
# TESTS DES ACTIONS INVALIDES
# ============================================================

def test_move_without_takeoff():
    """
    move_step doit être refusée si le drone n'est pas airborne.
    """
    g, env, agent = create_env_agent()

    old_state = env.get_state()

    assert agent.move_step() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_move_without_takeoff OK")


def test_avoid_without_takeoff():
    """
    avoid_maneuver doit être refusée si le drone n'est pas airborne.
    """
    g, env, agent = create_env_agent()

    old_state = env.get_state()

    assert agent.avoid_maneuver() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_avoid_without_takeoff OK")


def test_charge_without_docking():
    """
    charge_step doit être refusée si le drone n'est pas docked.
    """
    g, env, agent = create_env_agent()

    old_state = env.get_state()

    assert agent.charge_step() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_charge_without_docking OK")


def test_undock_without_docking():
    """
    undock_cmd doit être refusée si le drone n'est pas docked.
    """
    g, env, agent = create_env_agent()

    old_state = env.get_state()

    assert agent.undock_cmd() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_undock_without_docking OK")


def test_takeoff_when_already_airborne():
    """
    takeoff_cmd doit être refusée si le drone est déjà airborne.
    """
    g, env, agent = create_env_agent()

    assert agent.takeoff_cmd() == True

    old_state = env.get_state()

    assert agent.takeoff_cmd() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_takeoff_when_already_airborne OK")


def test_dock_not_at_base():
    """
    dock_cmd doit être refusée si le drone n'est pas à la base.
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    # On place volontairement le drone hors de la base
    env.posX = 1
    env.posY = 0
    env.check_invariant()

    old_state = env.get_state()

    assert agent.dock_cmd() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_dock_not_at_base OK")


def test_avoid_with_low_battery():
    """
    avoid_maneuver doit être refusée si la batterie est <= 1,
    car cette action coûte 2 unités de batterie.
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()
    env.battery = 1

    old_state = env.get_state()

    assert agent.avoid_maneuver() == False
    assert env.get_state() == old_state

    env.check_invariant()
    print("test_avoid_with_low_battery OK")


# ============================================================
# TESTS DE CRASH
# ============================================================

def test_crash_by_danger_update():
    """
    Si le drone se trouve sur une case dangereuse,
    update_obstacle_distance doit déclencher un crash.
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    env.posX = 3
    env.posY = 3

    env.update_obstacle_distance()

    assert env.crashed == 1
    assert env.airborne == 0
    assert env.obstacle_distance == 0
    assert env.is_terminal() == True

    env.check_invariant()
    print("test_crash_by_danger_update OK")


def test_move_step_can_crash():
    """
    On force le choix aléatoire de move_step vers une case dangereuse
    pour vérifier que le crash est bien déclenché.

    Position de départ : (3, 2)
    Case dangereuse voisine : (3, 3)
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    env.posX = 3
    env.posY = 2
    env.check_invariant()

    old_choice = drone_module.r.choice

    try:
        drone_module.r.choice = lambda voisins: (3, 3)

        assert agent.move_step() == True

        assert env.posX == 3
        assert env.posY == 3
        assert env.crashed == 1
        assert env.airborne == 0
        assert env.obstacle_distance == 0
        assert env.is_terminal() == True

        env.check_invariant()
        print("test_move_step_can_crash OK")

    finally:
        drone_module.r.choice = old_choice


def test_emergency_stop_terminal():
    """
    emergency_stop doit mettre l'environnement dans un état terminal.
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    assert agent.emergency_stop() == True

    assert env.crashed == 1
    assert env.airborne == 0
    assert env.docked == 0
    assert env.is_terminal() == True

    env.check_invariant()
    print("test_emergency_stop_terminal OK")


# ============================================================
# TESTS DU RETOUR À LA BASE
# ============================================================

def test_return_home_one_step():
    """
    return_home doit rapprocher le drone de la base.

    Base : (0, 0)
    Position initiale forcée : (2, 2)
    Après return_home : (1, 1)
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    env.posX = 2
    env.posY = 2
    env.battery = 50
    env.check_invariant()

    old_battery = env.battery

    assert agent.return_home() == True

    assert env.posX == 1
    assert env.posY == 1
    assert env.battery == old_battery - 1
    assert env.crashed == 0

    env.check_invariant()
    print("test_return_home_one_step OK")


def test_return_home_until_base():
    """
    Plusieurs appels à return_home doivent ramener le drone à la base.
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    env.posX = 3
    env.posY = 2
    env.battery = 50
    env.check_invariant()

    while not env.at_base():
        assert agent.return_home() == True
        assert env.crashed == 0
        env.check_invariant()

    assert env.posX == env.baseX
    assert env.posY == env.baseY
    assert env.at_base() == True

    print("test_return_home_until_base OK")


def test_dock_after_return_home():
    """
    Après un retour à la base, dock_cmd doit être possible.
    """
    g, env, agent = create_env_agent()

    agent.takeoff_cmd()

    env.posX = 2
    env.posY = 1
    env.battery = 50
    env.check_invariant()

    while not env.at_base():
        assert agent.return_home() == True

    assert env.at_base() == True
    assert agent.dock_cmd() == True
    assert env.docked == 1
    assert env.airborne == 0

    env.check_invariant()
    print("test_dock_after_return_home OK")


# ============================================================
# LANCEMENT DE TOUS LES TESTS
# ============================================================

if __name__ == "__main__":
    print("\n=== TESTS DE BASE ===")
    test_initialisation()
    test_takeoff()
    test_move_step()
    test_avoid_maneuver()
    test_dock_charge()
    test_emergency_stop()

    print("\n=== TESTS DES ACTIONS INVALIDES ===")
    test_move_without_takeoff()
    test_avoid_without_takeoff()
    test_charge_without_docking()
    test_undock_without_docking()
    test_takeoff_when_already_airborne()
    test_dock_not_at_base()
    test_avoid_with_low_battery()

    print("\n=== TESTS DE CRASH ===")
    test_crash_by_danger_update()
    test_move_step_can_crash()
    test_emergency_stop_terminal()

    print("\n=== TESTS DU RETOUR À LA BASE ===")
    test_return_home_one_step()
    test_return_home_until_base()
    test_dock_after_return_home()

    print("\nTous les tests de conformité sont passés.")