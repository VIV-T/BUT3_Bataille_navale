from unittest import TestCase
from IA import IA
from Navire import FactoryNavire
from Grille import Grille
from copy import deepcopy

class TestTools(TestCase) :
    def setUp(self):
        # definir un plateau cible et une liste de navires
        cuirasse = FactoryNavire(nom="cuirassé", taille=4).get_navire()
        sous_marin = FactoryNavire(nom="sous-marin", taille=3).get_navire()
        torpilleur = FactoryNavire(nom="torpilleur", taille=2).get_navire()

        self.navires = {cuirasse, sous_marin, torpilleur}

        grille = Grille(5, 5)
        grille.create()


        self.plateau_cible = grille.get_plateau()
        
        self.plateau_cible_adjacence = deepcopy(self.plateau_cible)
        self.plateau_cible_adjacence[1][1].set_statut("hit")
        
        return super().setUp()
    
    def test_initialisation(self) :
        self.IA_debutant = IA(level="débutant")
        self.assertEqual("débutant", self.IA_debutant.get_level())
        self.IA_intermediaire = IA(level="intermédiaire")
        self.assertEqual("intermédiaire", self.IA_debutant.get_level())
        self.IA_avance = IA(level="avancé")
        self.assertEqual("avancé", self.IA_debutant.get_level())

        self.IA_test = IA(level="test")
        self.assertEqual("test", self.IA_debutant.get_level())


    ### Liste cas testable
    ## Debutant 
    # recuperation d'entier valide (entre 0 et taille_plateau)
    # Le caratere aleatoire ne permet pas de tester plus que cela (et ca n'a pas bcp d'interet btw)
    def test_play_debutant(self) :
        ligne, colonne = self.IA_debutant.play_debutant(plateau_cible=self.plateau_cible)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))


    ## Intermédiaire
    # comme pour "debutant" + ajout de la verification du caractere "croisé" des coord 
    #   => cf. regle utilisée dans la fonction elle mm
    # Possible en plus de tester le cas "chasse" :
    #       => Si on a touché au precedent tir, le comportement n'est plus aléatoire mais bel et bien predictible et donc testable.  
    # plateau_cible vierge => les coordonnees doivent suivre le critere "croisées"
    def test_play_intermediaire_cas_nominal(self) :
        ligne, colonne = self.IA_intermediaire.play_intermediaire(plateau_cible=self.plateau_cible, navires=self.navires)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))
        # vérification du critère
        self.assertEqual(ligne//2, colonne//2)


    # Cas 'chasse' : on cible on case adjacente à une case touchee 
    # Plateau_cible => touche en (1,1)
    def test_play_intermediaire_cas_adjacence(self) :
        ligne, colonne = self.IA_intermediaire.play_intermediaire(plateau_cible=self.plateau_cible_adjacence, navires=self.navires)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))
        # verification brute des coord => anticipable grace au comportement defini de la fonction
        self.assertEqual(0, ligne)
        self.assertEqual(1, colonne)



    ## Avancé 
    # Je pense qu'il est possible de tester un "scenario" de jeu complet, bien que cela n'ai pas bcp d'interet...
    # Si parrallelisation des calcul de config : tester la connexion au cluster (plus dans TestTools_IA...?)
    def test_play_avance_cas_nominal(self) :
        ligne, colonne = self.IA_avance.play_avance(plateau_cible=self.plateau_cible, navires=self.navires)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))


    ## Fonction : play_IA
    # Tester toutes les difficultées (cas nominaux) + cas limite : diff = 'test'
    # cas nominal : debutant
    def test_play_IA_debutant(self):
        ligne, colonne = self.IA_debutant.play_IA(plateau_cible=self.plateau_cible, navires=self.navires)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))


    # cas nominal : intermediaire
    def test_play_IA_intermediaire(self):
        ligne, colonne = self.IA_intermediaire.play_IA(plateau_cible=self.plateau_cible, navires=self.navires)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))


    # cas nominal : avance
    def test_play_IA_avance(self):
        ligne, colonne = self.IA_avance.play_IA(plateau_cible=self.plateau_cible, navires=self.navires)
        self.assertEqual(int, type(ligne))
        self.assertEqual(int, type(colonne))
    
    # cas limite
    def test_play_IA_test(self):
        try :
            self.IA_test.play_IA(plateau_cible=self.plateau_cible, navires=self.navires)
        except ValueError as err :
            self.assertEqual("Le niveau de l'IA n'est pas correctement défini.", str(err))