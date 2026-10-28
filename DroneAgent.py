import random as r


class DroneAgent:

    def __init__(self, EtatEnvironnement):
        self.env = EtatEnvironnement

    def takeoff_cmd(self):
        """
        Action : décollage du drone.

        Préconditions selon le sujet :
        - le drone ne doit pas être crashé ;
        - le drone ne doit pas déjà être en vol ;
        - le drone ne doit pas être docked ;
        - la batterie doit être strictement positive.

        Effet :
        - airborne passe à 1 ;
        - docked reste à 0 ;
        - obstacle_distance est mis à jour.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible takeoff: le drone est crashed")
            return False

        if e.airborne != 0:
            print("Impossible takeoff: le drone est déjà airborne")
            return False

        if e.docked != 0:
            print("Impossible takeoff: le drone est docked")
            return False

        if e.battery <= 0:
            print("Impossible takeoff: batterie faible")
            return False

        e.airborne = 1
        e.docked = 0

        e.update_obstacle_distance()
        e.check_invariant()

        return True

    def move_step(self):
        """
        Action : déplacement élémentaire.

        Le déplacement est non déterministe :
        le drone choisit aléatoirement une case voisine valide.

        Coût :
        - batterie -1.

        Risque :
        - si la case atteinte est dangereuse, update_obstacle_distance()
          déclenche le crash.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible move_step: le drone est crashed")
            return False

        if e.airborne != 1:
            print("Impossible move_step: le drone n'est pas airborne")
            return False

        if e.docked != 0:
            print("Impossible move_step: le drone est docked")
            return False

        if e.battery <= 0:
            print("Impossible move_step: batterie faible")
            return False

        voisins = []

        if e.posY < e.maxY:
            voisins.append((e.posX, e.posY + 1))

        if e.posY > 0:
            voisins.append((e.posX, e.posY - 1))

        if e.posX < e.maxX:
            voisins.append((e.posX + 1, e.posY))

        if e.posX > 0:
            voisins.append((e.posX - 1, e.posY))

        nextX, nextY = r.choice(voisins)

        e.posX = nextX
        e.posY = nextY
        e.battery -= 1

        e.visZones.add(e.get_zone(nextX, nextY))

        e.update_obstacle_distance()
        e.check_invariant()

        return True

    def avoid_maneuver(self):
        """
        Action : manœuvre d'évitement.

        Différence avec move_step :
        - move_step choisit un voisin quelconque ;
        - avoid_maneuver privilégie un voisin non dangereux si possible.

        Coût :
        - batterie -2.

        Cette action représente le compromis sécurité / énergie demandé
        dans le sujet.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible avoid_maneuver: le drone est crashed")
            return False

        if e.airborne != 1:
            print("Impossible avoid_maneuver: le drone n'est pas airborne")
            return False

        if e.docked != 0:
            print("Impossible avoid_maneuver: le drone est docked")
            return False

        if e.battery <= 1:
            print("Impossible avoid_maneuver: batterie faible")
            return False

        voisins = []

        if e.posY < e.maxY:
            voisins.append((e.posX, e.posY + 1))

        if e.posY > 0:
            voisins.append((e.posX, e.posY - 1))

        if e.posX < e.maxX:
            voisins.append((e.posX + 1, e.posY))

        if e.posX > 0:
            voisins.append((e.posX - 1, e.posY))

        voisins_surs = []

        for (x, y) in voisins:
            if (x, y) not in e.grille.Danger:
                voisins_surs.append((x, y))

        if voisins_surs:
            nextX, nextY = r.choice(voisins_surs)
        else:
            nextX, nextY = r.choice(voisins)

        e.posX = nextX
        e.posY = nextY
        e.battery -= 2

        e.visZones.add(e.get_zone(nextX, nextY))

        e.update_obstacle_distance()
        e.check_invariant()

        return True

    def return_home(self):
        """
        Action : retour vers la base.

        Le drone effectue un pas qui rapproche sa position de la base.

        Coût :
        - batterie -1.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible return_home: le drone est crashed")
            return False

        if e.airborne != 1:
            print("Impossible return_home: le drone n'est pas airborne")
            return False

        if e.docked != 0:
            print("Impossible return_home: le drone est docked")
            return False

        if e.battery <= 0:
            print("Impossible return_home: batterie faible")
            return False

        if e.posX < e.baseX:
            nextX = e.posX + 1
        elif e.posX > e.baseX:
            nextX = e.posX - 1
        else:
            nextX = e.posX

        if e.posY < e.baseY:
            nextY = e.posY + 1
        elif e.posY > e.baseY:
            nextY = e.posY - 1
        else:
            nextY = e.posY

        e.posX = nextX
        e.posY = nextY
        e.battery -= 1

        e.visZones.add(e.get_zone(nextX, nextY))

        e.update_obstacle_distance()
        e.check_invariant()

        return True

    def dock_cmd(self):
        """
        Action : arrimage à la base.

        Préconditions :
        - drone non crashé ;
        - drone en vol ;
        - drone non docked ;
        - drone à la position de la base.

        Effet :
        - docked = 1 ;
        - airborne = 0.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible dock_cmd: le drone est crashed")
            return False

        if e.airborne != 1:
            print("Impossible dock_cmd: le drone n'est pas airborne")
            return False

        if e.docked != 0:
            print("Impossible dock_cmd: le drone est déjà docked")
            return False

        if not (e.posX == e.baseX and e.posY == e.baseY):
            print("Impossible dock_cmd: le drone n'est pas à la base")
            return False

        e.docked = 1
        e.airborne = 0

        e.check_invariant()

        return True

    def undock_cmd(self):
        """
        Action : sortie de l'état docked.

        Préconditions :
        - drone non crashé ;
        - drone docked ;
        - batterie > 0.

        Effet :
        - docked = 0 ;
        - airborne = 1.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible undock_cmd: le drone est crashed")
            return False

        if e.docked != 1:
            print("Impossible undock_cmd: le drone n'est pas docked")
            return False

        if e.battery <= 0:
            print("Impossible undock_cmd: batterie insuffisante")
            return False

        e.docked = 0
        e.airborne = 1

        e.visZones.add(e.get_zone(e.posX, e.posY))

        e.check_invariant()

        return True

    def charge_step(self):
        """
        Action : recharge progressive.

        Préconditions :
        - drone non crashé ;
        - drone docked.

        Effet :
        - batterie +5 jusqu'à un maximum de 100.
        """
        e = self.env

        if e.crashed != 0:
            print("Impossible charge_step: le drone est crashed")
            return False

        if e.docked != 1:
            print("Impossible charge_step: le drone n'est pas docked")
            return False

        if e.battery <= 95:
            e.battery += 5
        else:
            e.battery = 100

        e.check_invariant()

        return True

    def emergency_stop(self):
        """
        Action : arrêt d'urgence.

        Cette action peut être déclenchée à tout moment.

        Effet :
        - crashed = 1 ;
        - airborne = 0 ;
        - docked = 0 ;
        - obstacle_distance = 0.
        """
        e = self.env

        e.crashed = 1
        e.airborne = 0
        e.docked = 0
        e.obstacle_distance = 0

        e.check_invariant()

        return True