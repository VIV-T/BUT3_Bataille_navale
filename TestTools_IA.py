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
    # Tester les fonction individuellement dans l'ordre suivant :

    ## generation de toutes les configurations possible
    # - est_valide()    # a quoi sert precisement cette fonction btw ?
    #       - tester cas nominal
    #       - tester cas limite : pour chaque 'return False'   
    # - placer_navire()
    #       - tester cas nominal (la fnctn n'est appelée que dans ce cas)
    # - retirer_navire()
    #       - tester cas nominal (la fnctn n'est appelée que dans ce cas)
    # - configuration_valide()
    #       - tester cas nominal
    #       - tester cas limite : pour chaque 'return False'   
    # - generer_configurations()
    #       - tester plusieurs taille de plateaux
    #       - tester cas nominal sur plusieurs plateaux : vide et deja ciblé

    
    ## creation de la matrice de densite de proba 
    # - analyse_config()
    #       - tester cas nominal + cas vide ?
    # - genere_matrice_proba()
    #       - tester cas nominal + cas vide ?
    # - get_coord_from_matrice_proba()
    #       - tester cas nominal + cas vide ?
    