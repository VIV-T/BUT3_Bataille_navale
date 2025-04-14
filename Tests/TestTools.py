from unittest import TestCase
from Scripts.Tools import get_plateau_symbole, afficher_plateau, afficher_couple_plateau


class TestTools(TestCase) : 
    def setUp(self):
        # definir des plateaux (2 a chaque fois) de tailles differentes
        return super().setUp()
    
    ### Liste des tests possibles :
    ## get_plateau_symbole
    # - cas vide
    # - cas rempli (strategie)
    # - cas avec des tirs (fail & hit)

    ## afficher_plateau
    # tester differentes tailles de plateau pour les afficher, 
    # vide, rempli, avec fail & hit

    ## afficher_couple_plateaux
    # tester differentes tailles de plateau pour les afficher, 
    # vide, rempli, avec fail & hit