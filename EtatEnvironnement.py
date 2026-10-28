

class EtatEnvironnement :

    def __init__(self, Grille):
     
        self.baseX = 0
        self.baseY = 0
        
        self.grille = Grille
        self.maxX = Grille.MaxX
        self.maxY = Grille.MaxY
        
        # variables representant la position courante du drone dans la grille
        self.posX = self.baseX # = 0
        self.posY = self.baseY # = 0
        
        # niveau de batterie du drone entre 0 et 100
        self.battery = 100
        
        # represente la distance entre le drone et l'obstacle a chaque position
        self.obstacle_distance = 2
        
        #etat operationnel du drone 1 = True, 0 = False
        self.docked = 0 
        self.airborne = 0
        self.crashed = 0

        # ensemble de zone visite
        self.visZones = {self.grille.ZoneOf(self.posX,self.posY)}
        
        self.check_invariant()
        
    # methode pour verifier les invariants apres chaque mouvement du drone, incluant l'etat initial
    def check_invariant(self):

        assert 0 <= self.posX <= self.maxX, "posX hors limites"
        assert 0 <= self.posY <= self.maxY, "posY hors limites"

        assert 0 <= self.battery <= 100, "battery hors limites"

        assert self.docked in (0,1), "docked invalide"
        assert self.airborne in (0,1), "airborne invalide"
        assert self.crashed in (0,1), "crashed invalide"

        for z in self.visZones:
            assert 1 <= z <= self.grille.ZoneCount, "visZones hors limites"

        # contraintes logiques
        if self.docked == 1:
            assert self.airborne == 0, "docked=1 => airborne=0"
            assert self.posX == self.baseX and self.posY == self.baseY, "docked => position base"

        if self.crashed == 1:
            assert self.airborne == 0, "crashed=1 => airborne=0"
    
    def update_obstacle_distance(self):
        if (self.posX, self.posY) in self.grille.Danger:
            self.obstacle_distance = 0
            self.crashed = 1
            self.airborne = 0
        else:
            self.obstacle_distance = 2
        
    def get_zone(self, x, y):
        return self.grille.ZoneOf(x, y)
    
    def afficher(self):
        self.grille.afficher(self.posX, self.posY)
        
    def get_state(self):
        """
        Retourne une représentation complète de l'état courant.

        Cette méthode est utile pour :
        - afficher l'état ;
        - comparer deux états ;
        - construire l'espace d'états dans le mode exhaustif ;
        - préparer l'utilisation future avec un algorithme RL.
        """
        return (
            self.posX,
            self.posY,
            self.battery,
            self.obstacle_distance,
            self.docked,
            self.airborne,
            self.crashed,
            tuple(sorted(self.visZones))
        )

    def is_terminal(self):
        """
        Indique si l'état courant est terminal.

        Un état terminal est un état où l'épisode doit s'arrêter :
        - crash ;
        - batterie vide ;
        - mission terminée.
        """
        if self.crashed == 1:
            return True

        if self.battery <= 0:
            return True

        if self.mission_success():
            return True

        return False

    def at_base(self):
        """
        Vérifie si le drone est à la base.
        """
        return self.posX == self.baseX and self.posY == self.baseY

    def all_zones_visited(self):
        """
        Vérifie si toutes les zones de patrouille ont été visitées.
        """
        return len(self.visZones) == self.grille.ZoneCount

    def mission_success(self):
        """
        La mission est réussie si :
        - toutes les zones sont visitées ;
        - le drone est revenu à la base ;
        - le drone n'est pas crashé.
        """
        return self.all_zones_visited() and self.at_base() and self.crashed == 0

    def voisins_valides(self):
        """
        Retourne la liste des cellules voisines valides.

        Ces voisins correspondent aux déplacements haut, bas, droite, gauche,
        en restant dans les bornes de la grille.
        """
        voisins = []

        if self.posY < self.maxY:
            voisins.append((self.posX, self.posY + 1))

        if self.posY > 0:
            voisins.append((self.posX, self.posY - 1))

        if self.posX < self.maxX:
            voisins.append((self.posX + 1, self.posY))

        if self.posX > 0:
            voisins.append((self.posX - 1, self.posY))

        return voisins

    def voisins_surs(self):
        """
        Retourne les voisins qui ne sont pas dans Danger.
        """
        return [
            (x, y)
            for (x, y) in self.voisins_valides()
            if (x, y) not in self.grille.Danger
        ]
    
    def actions_possibles(self):
        """
        Retourne la liste des actions autorisées dans l'état courant.

        Cette méthode centralise les préconditions des opérations.
        """
        actions = []

        # takeoff_cmd
        if self.crashed == 0 and self.airborne == 0 and self.docked == 0 and self.battery > 0:
            actions.append("takeoff_cmd")

        # move_step
        if self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 0:
            actions.append("move_step")

        # avoid_maneuver
        if self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 1:
            actions.append("avoid_maneuver")

        # return_home
        if self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 0:
            actions.append("return_home")

        # dock_cmd
        if (
            self.crashed == 0
            and self.airborne == 1
            and self.docked == 0
            and self.posX == self.baseX
            and self.posY == self.baseY
        ):
            actions.append("dock_cmd")

        # undock_cmd
        if self.crashed == 0 and self.docked == 1 and self.battery > 0:
            actions.append("undock_cmd")

        # charge_step
        if self.crashed == 0 and self.docked == 1:
            actions.append("charge_step")

        # emergency_stop est toujours possible
        actions.append("emergency_stop")

        return actions
    
    def clone(self):
        """
        Crée une copie indépendante de l'environnement.

        Nécessaire pour explorer plusieurs transitions sans modifier
        l'environnement original.
        """
        new_env = EtatEnvironnement(self.grille)

        new_env.baseX = self.baseX
        new_env.baseY = self.baseY
        new_env.posX = self.posX
        new_env.posY = self.posY
        new_env.battery = self.battery
        new_env.obstacle_distance = self.obstacle_distance
        new_env.docked = self.docked
        new_env.airborne = self.airborne
        new_env.crashed = self.crashed
        new_env.visZones = set(self.visZones)

        new_env.check_invariant()
        return new_env