class Grille:
    def __init__(self, maxY, maxX):
        """
        Grille 2D discrète.

        maxX : coordonnée maximale en x
        maxY : coordonnée maximale en y

        Les cellules valides sont :
        x ∈ [0, maxX]
        y ∈ [0, maxY]
        """
        self.MaxY = maxY
        self.MaxX = maxX

        # Ensemble des cellules dangereuses.
        # Si le drone entre dans une de ces cellules, il risque un crash.
        self.Danger = {(3, 3), (4, 5), (5, 4)}

        # Le sujet impose 4 zones de patrouille.
        self.ZoneCount = 4

    def ZoneOf(self, x, y):
        """
        Retourne la zone de patrouille de la cellule (x, y).

        Découpage :
        zone 1 : x <= maxX/2 et y <= maxY/2
        zone 2 : x <= maxX/2 et y >  maxY/2
        zone 3 : x >  maxX/2 et y <= maxY/2
        zone 4 : x >  maxX/2 et y >  maxY/2
        """
        midX = self.MaxX // 2
        midY = self.MaxY // 2

        if x <= midX and y <= midY:
            return 1
        elif x <= midX and y > midY:
            return 2
        elif x > midX and y <= midY:
            return 3
        else:
            return 4

    def afficher(self, droneX=None, droneY=None):
        """
        Affiche la grille :
        D = drone
        X = danger
        . = cellule normale
        """
        for y in range(0, self.MaxY + 1):
            for x in range(0, self.MaxX + 1):
                if (x, y) == (droneX, droneY):
                    print("D", end=" ")
                elif (x, y) in self.Danger:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print()