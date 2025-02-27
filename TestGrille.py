import unittest
from Grille import Grille, afficher_grille, afficher_couple_grilles


class TestGrille(unittest.TestCase):
    grille: Grille

    # Creation - initialisation + self.create
    def test_creation_grille_cas_nominal(self) -> None:
        self.grille: Grille = Grille(10, 10)
        self.assertEqual(True, self.grille.create())
        self.assertEqual(
            [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']], self.grille.plateau)
        self.assertEqual(10, self.grille.get_nb_lignes())
        self.assertEqual(10, self.grille.get_nb_colonnes())

    def test_creation_grille_cas_nul_lignes(self) -> None:
        self.grille: Grille = Grille(0, 10)
        try:
            self.grille.create()
        except ValueError as current_error:
            self.assertEqual("Impossible de créer la grille !\n La valeur du nombre de lignes est incorrecte !",
                             str(current_error))
        self.assertEqual([], self.grille.plateau)
        self.assertEqual(None, self.grille.get_nb_lignes())
        self.assertEqual(10, self.grille.get_nb_colonnes())

    def test_creation_grille_cas_nul_colonnes(self) -> None:
        self.grille: Grille = Grille(10, 0)
        try:
            self.grille.create()
        except ValueError as current_error:
            self.assertEqual("Impossible de créer la grille !\n La valeur du nombre de colonnes est incorrecte !",
                             str(current_error))
        self.assertEqual([], self.grille.plateau)
        self.assertEqual(10, self.grille.get_nb_lignes())
        self.assertEqual(None, self.grille.get_nb_colonnes())

    def test_creation_grille_cas_negatif_lignes(self) -> None:
        self.grille: Grille = Grille(-1, 3)
        try:
            self.grille.create()
        except ValueError as current_error:
            self.assertEqual("Impossible de créer la grille !\n La valeur du nombre de lignes est incorrecte !",
                             str(current_error))

        self.assertEqual([], self.grille.plateau)
        self.assertEqual(None, self.grille.get_nb_lignes())
        self.assertEqual(3, self.grille.get_nb_colonnes())

    def test_creation_grille_cas_negatif_colonnes(self) -> None:
        self.grille: Grille = Grille(3, -1)
        try:
            self.grille.create()
        except ValueError as current_error:
            self.assertEqual("Impossible de créer la grille !\n La valeur du nombre de colonnes est incorrecte !",
                             str(current_error))

        self.assertEqual([], self.grille.plateau)
        self.assertEqual(3, self.grille.get_nb_lignes())
        self.assertEqual(None, self.grille.get_nb_colonnes())

    # __eq__
    def test__eq__cas_nominal(self):
        self.grille = Grille(10, 10)
        self.grille.create()
        self.grille_2 = Grille(10, 10)
        self.grille_2.create()
        self.assertTrue(self.grille == self.grille_2)

    def test__eq__cas_False(self):
        self.grille = Grille(10, 10)
        self.grille.create()
        self.grille_2 = Grille(5, 5)
        self.grille_2.create()
        self.assertFalse(self.grille == self.grille_2)

    ## Setters & Getters
    # lignes
    def test_setter_nb_lignes_cas_nominal(self) -> None:
        self.grille = Grille(10, 10)
        try:
            self.grille.set_nb_lignes(self.grille.nombre_lignes)
        except ValueError as current_error:
            self.assertEqual(f"Le nombre de lignes minimum est {self.grille.taille_min} !", str(current_error))
        self.assertEqual(10, self.grille.get_nb_lignes())

    def test_setter_nb_lignes_cas_nul(self) -> None:
        self.grille = Grille(0, 0)
        try:
            self.grille.set_nb_lignes(self.grille.nombre_lignes)
        except ValueError as current_error:
            self.assertEqual(f"Le nombre de lignes minimum est {self.grille.taille_min} !", str(current_error))
        self.assertEqual(None, self.grille.get_nb_lignes())

    def test_setter_nb_lignes_cas_negatif(self) -> None:
        self.grille = Grille(-1, -1)
        try:
            self.grille.set_nb_lignes(self.grille.nombre_lignes)
        except ValueError as current_error:
            self.assertEqual(f"Le nombre de lignes minimum est {self.grille.taille_min} !", str(current_error))
        self.assertEqual(None, self.grille.get_nb_lignes())

    # colonnes
    def test_setter_nb_colonnes_cas_nominal(self) -> None:
        self.grille = Grille(10, 10)
        try:
            self.grille.set_nb_colonnes(self.grille.nombre_colonnes)
        except ValueError as current_error:
            self.assertEqual(f"Le nombre de colonnes minimum est {self.grille.taille_min} !", str(current_error))
        self.assertEqual(10, self.grille.get_nb_colonnes())

    def test_setter_nb_colonnes_cas_nul(self) -> None:
        self.grille = Grille(0, 0)
        try:
            self.grille.set_nb_colonnes(self.grille.nombre_colonnes)
        except ValueError as current_error:
            self.assertEqual(f"Le nombre de colonnes minimum est {self.grille.taille_min} !", str(current_error))
        self.assertEqual(None, self.grille.get_nb_colonnes())

    def test_setter_nb_colonnes_cas_negatif(self) -> None:
        self.grille = Grille(-1, -1)
        try:
            self.grille.set_nb_colonnes(self.grille.nombre_colonnes)
        except ValueError as current_error:
            self.assertEqual(f"Le nombre de colonnes minimum est {self.grille.taille_min} !", str(current_error))
        self.assertEqual(None, self.grille.get_nb_colonnes())

    ## Méthodes de classe
    # afficher_grille
    def test_afficher_grille_10_10(self) -> None:
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
                          "- - - - - - - - - -\n"), afficher_grille(self.grille.plateau))

    def test_afficher_grille_10_5(self) -> None:
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
                          "- - - - -\n"), afficher_grille(self.grille.plateau))

    def test_afficher_grille_5_10(self) -> None:
        self.grille = Grille(5, 10)
        self.grille.create()
        self.assertEqual(("- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"
                          "- - - - - - - - - -\n"), afficher_grille(self.grille.plateau))

    # afficher_couple_grille
    def test_afficher_couple_grilles_2_10_10(self):
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
            afficher_couple_grilles(self.grille1.plateau, self.grille2.plateau))

    def test_afficher_couple_grilles_2_5_5(self):
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
            afficher_couple_grilles(self.grille1.plateau, self.grille2.plateau))

    def test_afficher_couple_grilles_tailles_differentes_lignes(self):
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
                afficher_couple_grilles(self.grille1.plateau, self.grille2.plateau))
        except ValueError as current_error:
            self.assertEqual("Les deux grilles sont de tailles différentes !", str(current_error))

    def test_afficher_couple_grilles_tailles_differentes_colonnes(self):
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
                afficher_couple_grilles(self.grille1.plateau, self.grille2.plateau))
        except ValueError as current_error:
            self.assertEqual("Les deux grilles sont de tailles différentes !", str(current_error))

    # reinit_plateau
    def test_reinit_plateau_cas_nominal(self):
        # initialisation d'une grille
        self.grille = Grille(10, 10)
        # Ne pas appeler la methode 'create' ! elle fait appelle à la méthode que nous souhaitons tester !

        self.assertEqual([['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']], self.grille.reinit_plateau())
