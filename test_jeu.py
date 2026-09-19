"""Tests automatises pour l'affichage du mot avec tirets."""

import unittest

from jeu import afficher_mot


class TestAfficherMot(unittest.TestCase):

    def test_aucune_lettre_trouvee(self):
        self.assertEqual(afficher_mot("chat", set()), "_ _ _ _")

    def test_toutes_les_lettres_trouvees(self):
        self.assertEqual(afficher_mot("chat", {"c", "h", "a", "t"}), "c h a t")

    def test_lettres_partiellement_trouvees(self):
        self.assertEqual(afficher_mot("chat", {"c", "a"}), "c _ a _")


if __name__ == "__main__":
    unittest.main()