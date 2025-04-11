from unittest import TestCase
from IA import IA

class TestTools(TestCase) :
    def setUp(self):
        # definir un plateau cible et une liste de navires
        return super().setUp()
    
    def test_initialisation(self) :
        self.IA_debutant = IA(level="débutant")
        self.assertEqual("débutant", self.IA_debutant.get_level())

    ### Liste cas testable
    ## Debutant 
    # recuperation d'entier valide (entre 0 et taille_plateau)
    # Le caratere aleatoire ne permet pas de tester plus que cela (et ca n'a pas bcp d'interet btw)

    ## Intermédiaire
    # comme pour "debutant" + ajout de la verification du caractere "croisé" des coord 
    #   => cf. regle utilisée dans la fonction elle mm
    # Possible en plus de tester le cas "chasse" :
    #       => Si on a touché au precedent tir, le comportement n'est plus aléatoire mais bel et bien predictible et donc testable.

    ## Avancé 
    # Je pense qu'il est possible de tester un "scenario" de jeu complet, bien que cela n'ai pas bcp d'interet...
    # Si parrallelisation des calcul de config : tester la connexion au cluster (plus dans TestTools_IA...?)