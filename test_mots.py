"""Tests automatises pour la selection des mots et le respect de la difficulte."""

import unittest

from mots import choisir_mot, CATEGORIES, DIFFICULTES


class TestChoisirMot(unittest.TestCase):

    def test_mot_appartient_a_la_categorie(self):
        """Le mot choisi doit toujours faire partie de la categorie demandee."""
        for categorie in CATEGORIES:
            mot = choisir_mot(categorie, "moyen")
            self.assertIn(mot, CATEGORIES[categorie])

    def test_longueur_respecte_la_difficulte(self):
        """La longueur du mot choisi doit respecter la plage de la difficulte."""
        for categorie in CATEGORIES:
            for difficulte, (min_len, max_len) in DIFFICULTES.items():
                mot = choisir_mot(categorie, difficulte)
                self.assertTrue(
                    min_len <= len(mot) <= max_len,
                    f"'{mot}' ({len(mot)} lettres) hors de la plage '{difficulte}'",
                )

    def test_categorie_inexistante_leve_une_erreur(self):
        """Choisir une categorie qui n'existe pas doit lever une erreur claire."""
        with self.assertRaises(KeyError):
            choisir_mot("categorie_qui_nexiste_pas", "facile")


if __name__ == "__main__":
    unittest.main()