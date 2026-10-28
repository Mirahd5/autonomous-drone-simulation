class Simulation:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def execute_action(self, action):
        """
        Exécute une action donnée sous forme de chaîne de caractères.

        Retourne True si l'action est exécutée,
        False sinon.
        """
        if action not in self.env.actions_possibles():
            print("Action non autorisée :", action)
            return False

        if action == "takeoff_cmd":
            return self.agent.takeoff_cmd()

        if action == "move_step":
            return self.agent.move_step()

        if action == "avoid_maneuver":
            return self.agent.avoid_maneuver()

        if action == "return_home":
            return self.agent.return_home()

        if action == "dock_cmd":
            return self.agent.dock_cmd()

        if action == "undock_cmd":
            return self.agent.undock_cmd()

        if action == "charge_step":
            return self.agent.charge_step()

        if action == "emergency_stop":
            return self.agent.emergency_stop()

        print("Action inconnue :", action)
        return False