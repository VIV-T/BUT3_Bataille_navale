from unittest import TestCase

from Scripts.Grille import Grille
from Scripts.Tools import get_plateau_symbole, afficher_plateau, afficher_couple_plateau
from Scripts.Navire import FactoryNavire


class TestTools(TestCase) :
    def setUp(self):
        # definir des plateaux (2 a chaque fois) de tailles differentes
        return super().setUp()

    ### Liste des tests possibles :
    ## get_plateau_symbole
    # - cas vide
    # - cas rempli (strategie)
    # - cas avec des tirs (fail & hit)
    def test_get_plateau_symbole_cas_vide(self):
        self.grille = Grille(10, 10)
        self.grille.create()
        self.assertEqual([['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]
                         , get_plateau_symbole(self.grille.get_plateau()))

    def test_get_plateau_symbole_cas_hit_fail(self):
        self.grille = Grille(10, 10)
        self.grille.create()
        self.grille.get_plateau()[0][0].set_statut("hit")
        self.grille.get_plateau()[2][2].set_statut("fail")
        self.assertEqual([['X', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '0', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]
                         , get_plateau_symbole(self.grille.get_plateau()))

    def test_get_plateau_symbole_en_jeu(self):
        self.grille = Grille(10, 10)
        self.grille.create()

        # On plqce le nqvire sur le plateau
        torpilleur = FactoryNavire(nom="torpilleur", taille=2).get_navire()
        self.grille.get_plateau()[0][0].set_navire(torpilleur)
        self.grille.get_plateau()[0][1].set_navire(torpilleur)

        # Tir su le navire et dans le vide
        self.grille.get_plateau()[0][0].set_statut("hit")
        self.grille.get_plateau()[2][2].set_statut("fail")

        self.assertEqual([['X', 'T', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '0', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]
                         , get_plateau_symbole(self.grille.get_plateau()))


        ## afficher_plateau
    def test_afficher_plateau_10_10(self) -> None:
        self.grille = Grille(10, 10)
        self.grille.create()
        self.assertEqual(("- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"), afficher_plateau(self.grille.get_plateau()))

    def test_afficher_plateau_10_5(self) -> None:
        self.grille = Grille(10, 5)
        self.grille.create()
        self.assertEqual(("- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"
                          "- - - - -\n"), afficher_plateau(self.grille.get_plateau()))

    def test_afficher_plateau_5_10(self) -> None:
        self.grille = Grille(5, 10)
        self.grille.create()
        self.assertEqual(("- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"), afficher_plateau(self.grille.get_plateau()))

    ## afficher_couple_plateaux
    def test_afficher_couple_plateaux_2_10_10(self):
        # intialisation des grilles
        self.grille1 = Grille(10, 10)
        self.grille2 = Grille(10, 10)
        # creation des plateau
        self.grille1.create()
        self.grille2.create()
        # test sur l'affichage simultané des 2 grilles
        self.assertEqual((
            "     Vos navires :                      Champ de tir :\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"
            "     - - - - - - - - - -                - - - - - - - - - -\n"),
            afficher_couple_plateau(self.grille1.get_plateau(), self.grille2.get_plateau()))

    def test_afficher_plateaux_grilles_2_5_5(self):
        # intialisation des grilles
        self.grille1 = Grille(5, 5)
        self.grille2 = Grille(5, 5)
        # creation des plateau
        self.grille1.create()
        self.grille2.create()
        # test sur l'affichage simultané des 2 grilles
        self.assertEqual(
            "     Vos navires :                      Champ de tir :\n"
            "     - - - - -                - - - - -\n"
            "     - - - - -                - - - - -\n"
            "     - - - - -                - - - - -\n"
            "     - - - - -                - - - - -\n"
            "     - - - - -                - - - - -\n",
            afficher_couple_plateau(self.grille1.get_plateau(), self.grille2.get_plateau()))

    def test_afficher_couple_plateaux_tailles_differentes_lignes(self):
        # intialisation des grilles
        self.grille1 = Grille(10, 10)
        self.grille2 = Grille(10, 5)
        # creation des plateau
        self.grille1.create()
        self.grille2.create()
        # test sur l'affichage simultané des 2 grilles
        try:
            self.assertEqual((
                "     Vos navires :                      Champ de tir :\n"
                "     - - - - - - - - - -                - - - - - - - - - -\n"
                "     - - - - - - - - - -                - - - - - - - - - -\n"
                "     - - - - - - - - - -                - - - - - - - - - -\n"
                "     - - - - - - - - - -                - - - - - - - - - -\n"
                "     - - - - - - - - - -                - - - - - - - - - -\n"
                "                                        - - - - - - - - - -\n"
                "                                        - - - - - - - - - -\n"
                "                                        - - - - - - - - - -\n"
                "                                        - - - - - - - - - -\n"
                "                                        - - - - - - - - - -\n"),
                afficher_couple_plateau(self.grille1.get_plateau(), self.grille2.get_plateau()))
        except ValueError as current_error:
            self.assertEqual("Les deux grilles sont de tailles différentes !", str(current_error))

    def test_afficher_couple_plateaux_tailles_differentes_colonnes(self):
        # intialisation des grilles
        self.grille1 = Grille(10, 10)
        self.grille2 = Grille(10, 5)
        # creation des plateau
        self.grille1.create()
        self.grille2.create()
        # test sur l'affichage simultané des 2 grilles
        try:
            self.assertEqual((
                "     Vos navires :                      Champ de tir :\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"
                "     - - - - - - - - - -                - - - - -\n"),
                afficher_couple_plateau(self.grille1.get_plateau(), self.grille2.get_plateau()))
        except ValueError as current_error:
            self.assertEqual("Les deux grilles sont de tailles différentes !", str(current_error))