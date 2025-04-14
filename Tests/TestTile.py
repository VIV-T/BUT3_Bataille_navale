from unittest import TestCase

from Scripts.Tile import Tile


class TestTile(TestCase) :
    def test_set_navire(self):
        self.tile = Tile()
        self.tile.set_navire()

        self.assertEqual(None, self.tile.get_navire())

    def test_set_symbole(self):
        self.tile = Tile()
        self.tile.set_navire()
        self.tile.set_symbole()

        self.assertEqual("-", self.tile.get_symbole())


if __name__=="__main__" :
    test = TestTile()
    test.test_set_navire()
    test.test_set_symbole()