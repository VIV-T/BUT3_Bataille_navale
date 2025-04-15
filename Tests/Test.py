import unittest

from Tests.TestTile import TestTile
from Tests.TestGrille import TestGrille
from Tests.TestNavire import TestNavire
from Tests.TestStrategie import TestStrategie
from Tests.TestModeJeu import TestModeJeu
from Tests.TestCreationStrategie import TestCreationStrategie
from Tests.TestCreationModeJeu import TestCreationModeJeu
from Tests.TestChoixStrategie import TestChoixStrategie
from Tests.TestChoixModeJeu import TestChoixModeJeu
from Tests.TestBatailleNavale import TestBatailleNavale

from Tests.TestIA import TestIA
from Tests.TestTools import TestTools
from Tests.TestTools_IA import TestTools_IA


class Test(unittest.TestCase):
    def main(self):
        TestTile()
        TestTools()
        TestGrille()
        TestNavire()
        TestStrategie()
        TestModeJeu()

        # classes de creation
        TestCreationStrategie()
        TestCreationModeJeu()

        # classes de choix
        TestChoixStrategie()
        TestChoixModeJeu()

        # classe de jeu : BatailleNavale
        TestBatailleNavale()

        # IA et Tools associés
        TestIA()
        TestTools_IA()

if __name__ == '__main__':
    Test().main()
