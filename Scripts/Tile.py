"""
La classe Case permet d'instancier les élément qui compose la grille de jeu (cf. classe Grille)

Elle est particulièrement utile pour ce tout ce qui est relatif au calcul de probabilité de densité pour l'IA du jeu. 

Usage potentiellement utile pour toutes les question d'affichage.

"""

# Imports
from Scripts.Navire import Navire

# Classe 
class Tile() :
    # Variables privées
    _statut : str | None = None
    _navire : Navire | None
    _symbole : str 

    # Getters 
    def get_navire(self):
        return self._navire

    def get_symbole(self):
        return self._symbole


    def get_statut(self):
        return self._statut
    

    # Setters
    def set_navire(self, navire : Navire | None = None):
        if navire is None : 
            self._navire = None
        else :
            self._navire = navire

        self.set_symbole()
        return True


    def set_symbole(self, symbole : str | None = None):
        if symbole is None :
            if self._navire is None : 
                self._symbole = "-"
            else :
                self._symbole = self._navire.get_symbole()

        else :
            self._symbole = symbole

        return True


    def set_statut(self, statut : str | None = None, navire : Navire|None = None): 
            match statut :
                case None :
                    self._statut = None
                # raté
                case "fail" :
                    self._statut = "fail"
                    self.set_symbole("0")
                # touché
                case "hit" : 
                    self._statut = "hit"
                    # cas particulier : changement de la valeur de "self.navire" pour la grille d'attaque:
                    # permet de transferer l'information pour l'IA avance.
                    try :
                        if self.get_navire() is None and navire is not None :
                            self.set_navire(navire=navire)
                    except :
                        pass
                    self.set_symbole("X")
                # coulé
                case "cast" : 
                    self._statut = "cast"
                    # cas particulier : changement de la valeur de "self.navire" pour la grille d'attaque:
                    # permet de transferer l'information pour l'IA avance.
                    try :
                        if self.get_navire() is None and navire is not None :
                            self.set_navire(navire=navire)
                    except :
                        pass
                    self.set_symbole("X")

    # Constructeur
    def __init__(self, navire = None):
        pass 

    # important a definir pour pouvoir definir ensuite l'égalité des grilles
    def __eq__(self, other):
        pass

class FactoryTile() :
    def get_instance_tile(self) :
        return self.tile

    def __init__(self):
        self.tile = Tile()
        self.tile.set_navire()
        self.tile.set_symbole()
        