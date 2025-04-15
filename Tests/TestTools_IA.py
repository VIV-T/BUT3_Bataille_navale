from copy import deepcopy
from unittest import TestCase

import Scripts.Tools_IA as tools_ia
from Scripts.Grille import Grille
from Scripts.Navire import FactoryNavire
from Scripts.Tools import get_plateau_symbole

class TestTools_IA(TestCase) :
    def setUp(self):
        self.grille = Grille(10,10)
        self.grille.create()
        self.plateau_vide = self.grille.get_plateau()


        self.plateau_targeted = deepcopy(self.plateau_vide)
        # Tirs artificiels
        self.plateau_targeted[0][0].set_statut("hit")
        self.plateau_targeted[2][2].set_statut("fail")


        self.cuirasse = FactoryNavire(nom="cuirassé", taille=4).get_navire()
        self.fregate = FactoryNavire(nom="frégate", taille=3).get_navire()
        self.sous_marin = FactoryNavire(nom="sous-marin", taille=3).get_navire()
        self.torpilleur = FactoryNavire(nom="torpilleur", taille=2).get_navire()
        self.porte_avions = FactoryNavire(nom="porte-avions", taille=5).get_navire()

        self.navires = {self.cuirasse, self.fregate, self.sous_marin, self.torpilleur, self.porte_avions}

        return super().setUp()


    ## IA intermédiaire
    # trouver_coordonnees_ciblees
    def test_trouver_coordonnees_ciblees_vide(self):
        self.assertEqual([], tools_ia.trouver_coordonnees_ciblees(self.plateau_vide))

    def test_trouver_coordonnees_ciblees_hits_fails(self):
        self.assertEqual([(0,0),(2,2)], tools_ia.trouver_coordonnees_ciblees(self.plateau_targeted))


    # trouver_coord_case_adjacente
    def test_trouver_coord_case_adjacente_vide(self):
        self.assertEqual((-1,-1), tools_ia.trouver_coord_case_adjacente(self.plateau_vide))

    def test_trouver_coord_case_adjacente_hits_fails_1(self):
        self.assertEqual((1,0), tools_ia.trouver_coord_case_adjacente(self.plateau_targeted))

    def test_trouver_coord_case_adjacente_hits_fails_2(self):
        self.plateau_targeted_2 = deepcopy(self.plateau_vide)
        self.plateau_targeted_2[5][5].set_statut("hit")
        self.assertEqual((4,5), tools_ia.trouver_coord_case_adjacente(self.plateau_targeted_2))


    # cibler_coord_cross_random
    def test_cibler_coord_cross_random(self):
        coord_ciblee = tools_ia.cibler_coord_cross_random(self.plateau_vide,self.navires)
        self.assertEqual(int, type(coord_ciblee[0]))
        self.assertEqual(int, type(coord_ciblee[1]))



    ## IA avancé
    # check_nb_targeted_tile
    def test_check_nb_targeted_tile_0(self):
        self.assertEqual(0, tools_ia.check_nb_targeted_tile(self.plateau_vide))

    def test_check_nb_targeted_tile_2(self):
        self.assertEqual(2, tools_ia.check_nb_targeted_tile(self.plateau_targeted))



    # placement_navire_valide
    def test_placement_navire_valide_cas_nominal(self):
        placement_valide = tools_ia.placement_navire_valide(
            plateau_cible=self.plateau_vide,
            taille=self.torpilleur.get_taille(),
            colonne=0,
            ligne=0,
            horizontal=True)

        self.assertEqual(True, placement_valide)

    def test_placement_navire_valide_debordement_colonne_suivante(self):
        placement_valide = tools_ia.placement_navire_valide(
            plateau_cible=self.plateau_vide,
            taille=self.torpilleur.get_taille(),
            colonne=9,
            ligne=1,
            horizontal=True)

        self.assertEqual(False, placement_valide)

    def test_placement_navire_valide_chevauchement_colonne_suivante(self):
        self.plateau_targeted_3 = deepcopy(self.plateau_vide)
        self.plateau_targeted_3[5][5].set_statut("fail")
        placement_valide = tools_ia.placement_navire_valide(
            plateau_cible=self.plateau_targeted_3,
            taille=self.torpilleur.get_taille(),
            colonne=4,
            ligne=5,
            horizontal=True)

        self.assertEqual(False, placement_valide)


    def test_placement_navire_valide_debordement_ligne_suivante(self):
        placement_valide = tools_ia.placement_navire_valide(
            plateau_cible=self.plateau_vide,
            taille=self.torpilleur.get_taille(),
            colonne=1,
            ligne=9,
            horizontal=False)

        self.assertEqual(False, placement_valide)


    def test_placement_navire_valide_chevauchement_ligne_suivante(self):
        self.plateau_targeted_3 = deepcopy(self.plateau_vide)
        self.plateau_targeted_3[5][5].set_statut("fail")
        placement_valide = tools_ia.placement_navire_valide(
            plateau_cible=self.plateau_targeted_3,
            taille=self.torpilleur.get_taille(),
            colonne=5,
            ligne=4,
            horizontal=False)

        self.assertEqual(False, placement_valide)


    # placer_navire
    def test_placer_navire(self):
        tools_ia.placer_navire(navire=self.torpilleur, colonne=0, ligne=0, horizontal=True, plateau_cible=self.plateau_vide)
        self.assertEqual([['T', 'T', '-', '-', '-', '-', '-', '-', '-', '-'],
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


    # retirer_navire
    def test_retier_navire(self):
        tools_ia.placer_navire(navire=self.torpilleur, colonne=0, ligne=0, horizontal=True, plateau_cible=self.plateau_vide)
        # verification que le navire est correctement placé avant de le retirer
        self.assertEqual([['T', 'T', '-', '-', '-', '-', '-', '-', '-', '-'],
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
        tools_ia.retirer_navire(horizontal=True, grille=self.plateau_vide, taille=self.torpilleur.get_taille(), colonne=0, ligne=0)
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


    # configuration_valide
    def test_configuration_valide_true(self):
        tools_ia.placer_navire(plateau_cible=self.plateau_targeted, navire=self.torpilleur, colonne=0, ligne=0, horizontal=True)
        self.assertEqual(True,
                         tools_ia.configuration_valide(
                             plateau_cible=self.plateau_targeted,
                             navires={self.torpilleur},
                             nb_hits=1))

    def test_configuration_valide_false(self):
        tools_ia.placer_navire(plateau_cible=self.plateau_targeted, navire=self.torpilleur, colonne=4, ligne=4, horizontal=True)
        self.assertEqual(False,
                         tools_ia.configuration_valide(
                             plateau_cible=self.plateau_targeted,
                             navires={self.torpilleur},
                             nb_hits=1))


    # generer_configurations
    #       - tester plusieurs taille de plateaux
    #       - tester cas nominal sur plusieurs plateaux : vide et deja ciblé
    def test_generer_configurations_Blitz_vide(self):
        navires_blitz = {self.cuirasse, self.sous_marin, self.torpilleur}

        grille_blitz = Grille(5,5)
        grille_blitz.create()
        plateau_vide_blitz = grille_blitz.get_plateau()

        test_config = tools_ia.generer_configurations(plateau_cible=plateau_vide_blitz, navires=navires_blitz)

        self.assertEqual(len(test_config), 9024)

    def test_generer_configurations_Blitz_hits_fails(self):
        navires_blitz = {self.cuirasse, self.sous_marin, self.torpilleur}

        grille_blitz = Grille(5, 5)
        grille_blitz.create()
        plateau_vide_blitz = grille_blitz.get_plateau()

        # Tirs artificiels
        plateau_vide_blitz[0][0].set_statut("hit")
        plateau_vide_blitz[4][4].set_statut("hit")
        plateau_vide_blitz[4][0].set_statut("fail")
        plateau_vide_blitz[3][1].set_statut("fail")
        plateau_vide_blitz[0][4].set_statut("fail")

        test_config = tools_ia.generer_configurations(plateau_cible=plateau_vide_blitz, navires=navires_blitz)
        self.assertEqual(len(test_config), 340)


    def set_plateau_Normal_test_config(self):
        plateau = deepcopy(self.plateau_vide)
        # Tirs artificiels
        plateau[0][0].set_statut("cast", navire=self.torpilleur)
        plateau[0][1].set_statut("cast", navire=self.torpilleur)
        plateau[4][2].set_statut("hit", navire=self.sous_marin)
        plateau[4][0].set_statut("fail")
        plateau[3][1].set_statut("fail")
        plateau[0][4].set_statut("fail")
        plateau[9][9].set_statut("cast", navire=self.cuirasse)
        plateau[8][9].set_statut("cast", navire=self.cuirasse)
        plateau[7][9].set_statut("cast", navire=self.cuirasse)
        plateau[6][9].set_statut("cast", navire=self.cuirasse)
        plateau[0][9].set_statut("hit", navire=self.fregate)
        plateau[1][9].set_statut("hit", navire=self.fregate)
        plateau[8][3].set_statut("hit", navire=self.porte_avions)
        plateau[8][6].set_statut("hit", navire=self.porte_avions)
        plateau[0][7].set_statut("fail")
        plateau[5][5].set_statut("fail")
        plateau[6][6].set_statut("fail")
        plateau[5][7].set_statut("fail")
        plateau[4][6].set_statut("fail")
        plateau[8][8].set_statut("fail")
        plateau[6][8].set_statut("fail")
        plateau[9][7].set_statut("fail")
        plateau[7][7].set_statut("fail")
        plateau[9][5].set_statut("fail")
        plateau[2][2].set_statut("fail")
        plateau[2][4].set_statut("fail")
        plateau[2][6].set_statut("fail")
        plateau[5][1].set_statut("fail")
        plateau[6][4].set_statut("fail")
        plateau[8][0].set_statut("fail")
        plateau[5][3].set_statut("fail")
        plateau[9][1].set_statut("fail")
        plateau[8][2].set_statut("fail")
        plateau[9][3].set_statut("fail")

        return plateau


    def test_generer_configurations_Normal_hits_fails(self):
        plateau_normal = self.set_plateau_Normal_test_config()

        test_config = tools_ia.generer_configurations(plateau_cible=plateau_normal, navires=self.navires)
        self.assertEqual(len(test_config), 8)



    # analyse_config
    def test_analyse_config_cas_nominal(self):
        plateau_normal = self.set_plateau_Normal_test_config()
        configurations = tools_ia.generer_configurations(plateau_cible=plateau_normal, navires=self.navires)
        test_config_analysed = tools_ia.analyse_config(configurations)
        self.assertEqual(len(test_config_analysed), 8)


    def test_analyse_config_cas_vide(self):
        configurations = []
        test_config_analyzed = tools_ia.analyse_config(configurations)
        self.assertEqual(len(test_config_analyzed), 0)


    # genere_matrice_proba
    def test_genere_matrice_proba_cas_nominal(self):
        plateau_normal = self.set_plateau_Normal_test_config()
        configurations = tools_ia.generer_configurations(plateau_cible=plateau_normal, navires=self.navires)
        test_matrice_proba = tools_ia.genere_matrice_proba(configurations)
        self.assertEqual(test_matrice_proba,
                         [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                          [0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.25, 0.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])


    def test_genere_matrice_proba_cas_vide(self):
        configurations = []
        try :
            test_matrice_proba = tools_ia.genere_matrice_proba(configurations)
        except ZeroDivisionError as err :
            self.assertEqual(str(err), "division by zero")


    # get_coord_from_matrice_proba
    def test_get_coord_from_matrice_proba_cas_nominal(self):
        plateau_normal = self.set_plateau_Normal_test_config()
        configurations = tools_ia.generer_configurations(plateau_cible=plateau_normal, navires=self.navires)
        test_matrice_proba = tools_ia.genere_matrice_proba(configurations)
        ligne, colonne = tools_ia.get_coord_from_matrice_proba(test_matrice_proba)
        self.assertEqual(8, ligne)
        self.assertEqual(4, colonne)