from unittest import TestCase
# from Tools_IA import

class TestTools_IA(TestCase) :
    def setUp(self):
        return super().setUp()
    
    ##### Liste des tests possibles :
    #### IA intermédiaire
    ## trouver_coordonnees_ciblees
    # cas nominal : plateau avec des "hit" & "fail" 
    #   => renvoie la liste des coord
    # cas vide : renvoie une liste vide 

    ## trouver_coord_case_adjacente
    # cas nominal : renvoie les coord d'une case adjacente à une case "hit"
    # cas sans "hit" : renvoie (-1, -1)
    
    #### IA avancé 
    # 
    # 