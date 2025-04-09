"""
La classe grille permet de support pour le jeu.

Elle est appellée par (presque) toutes les autres classes.

Inputs :
    - nombre_lignes : le nombre de ligne de la grille
    - nombre_colonnes : le nombre de colonne de la grille

Il faut retenir qu'une grille de jeu est une matrice (= liste de liste).
Le nombre_lignes défini la longueur de la liste principale.
Le nombre_colonnes défini la longueur des listes secondaires.

La methode de classe self.create() permet de créer le plateau de jeu en fonction des critères d'initialisation.

la methode self.reinit_plateau permet de réinitialiser  le plateau de jeu (matrice), à partir des données d'initialisation.

Cette classe contient aussi deux méthodes d'affichage très utile notamment
pour la classe BatailleNavale() et pour la classe ChoixStrategie().
"""
from Tile import FactoryTile
from Tools import get_plateau_symbole

class Grille():
    # Variables privées
    __nb_lignes = 0
    __nb_colonnes = 0

    # Getters
    def get_nb_lignes(self):
        return self.__nb_lignes

    def get_nb_colonnes(self):
        return self.__nb_colonnes

    def get_plateau(self) -> list:
        return self.plateau

    # Setters
    def set_nb_lignes(self, nb_lignes: int):
        # test sur le nombre de ligne minimum et maximum défini par le programmeur
        if nb_lignes < self.taille_min:
            self.__nb_lignes = None
            raise ValueError(f"Le nombre de lignes minimum est {self.taille_min} !")
        elif nb_lignes > self.taille_max:
            self.__nb_lignes = None
            raise ValueError(f"Le nombre de lignes maximum est {self.taille_max} !")
        else:
            self.__nb_lignes = nb_lignes

    def set_nb_colonnes(self, nb_colonnes: int):
        # test sur le nombre de colonen minimum et maximum défini par le programmeur
        if nb_colonnes < self.taille_min:
            self.__nb_colonnes = None
            raise ValueError(f"Le nombre de colonnes minimum est {self.taille_min} !")
        elif nb_colonnes > self.taille_max:
            self.__nb_colonnes = None
            raise ValueError(f"Le nombre de colonnes maximum est {self.taille_max} !")
        else:
            self.__nb_colonnes = nb_colonnes

    # Constructeur
    def __init__(self, nombre_lignes, nombre_colonnes):
        self.taille_min: int = 2
        self.taille_max: int = 20
        self.nombre_colonnes = nombre_colonnes
        self.nombre_lignes = nombre_lignes

        self.plateau = []

    def reinit_plateau(self):
        # permet de recréer un plateau vierge à partir des données d'initialisation - réinitialisation du plateau.
        self.create()
        return self.plateau

    # Créer une grille de jeu:
    def create(self):
        # verifications de la validite du nb de lignes et de colonnes
        observateur = 0
        # Condition sur les lignes
        try:
            self.set_nb_lignes(nb_lignes=self.nombre_lignes)
        except:
            observateur = 1
            erreur = "lignes"
        # Condition sur les colonnes
        try:
            self.set_nb_colonnes(nb_colonnes=self.nombre_colonnes)
        except:
            observateur = 2
            erreur = "colonnes"
        # Return False si l'une des valeurs est non-conforme.
        if observateur > 0:
            raise ValueError(f"Impossible de créer la grille !\n La valeur du nombre de {erreur} est incorrecte !")

        # creation de la matrice (liste de listes) contenant des '-'
        self.plateau = []
        for i in range(self.__nb_lignes):
            self.plateau.append([])
            for j in range(self.__nb_colonnes):
                tile = FactoryTile().get_instance_tile()
                self.plateau[i].append(tile)

        return True

    def __eq__(self, other):
        if get_plateau_symbole(self.plateau) == get_plateau_symbole(other.plateau):
            return True
        return False



if __name__=="__main__" :
    grille = Grille(10, 10)
    grille.create()
    plateau1 = grille.get_plateau()
    plateau2 = grille.get_plateau()

    #afficher_plateau(plateau=plateau1)
    #afficher_couple_plateau(plateau1, plateau2)

    grille_bis = Grille(10, 10)
    grille_bis.create()


    if grille_bis == grille :
        print(True)