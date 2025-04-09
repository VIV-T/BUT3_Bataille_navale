"""
La classe Case permet d'instancier les élément qui compose la grille de jeu (cf. classe Grille)

Elle est particulièrement utile pour ce tout ce qui est relatif au calcul de probabilité de densité pour l'IA du jeu. 

Usage potentiellement utile pour toutes les question d'affichage.

"""

# Imports


# Classe 
class Case() :
    # Variables privées
    _statut : str | None
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
        return True


    def set_symbole(self):
        if self._navire is None : 
            self._symbole = "-"
        else :
            self._symbole = self._navire.get_symbole()
        return True


    def set_statut(self, status : str | None = None): 
            pass

    # Constructeur
    def __init__(self, navire = None):
        pass 

    # important a definir pour pouvoir definir ensuite l'égalité des grilles
    def __eq__(self, other):
        pass

class FactoryCase() :
    def get_instance_case(self) :
        return self.case

    def __init__(self):
        self.case = Case()
        # Apple des setters de cases avec les paramètres du constructeur.