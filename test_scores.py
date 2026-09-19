"""Tests automatises pour le calcul et la sauvegarde des scores."""

import os
import unittest

import scores


class TestCalculerScore(unittest.TestCase):

    def test_score_sans_erreur(self):
        """Un mot de 6 lettres sans erreur en facile doit donner 60 points."""
        self.assertEqual(scores.calculer_score("python", 0, "facile"), 60)

    def test_score_avec_erreurs(self):
        """Chaque erreur retire 5 points au score de base."""
        self.assertEqual(scores.calculer_score("python", 2, "facile"), 50)

    def test_score_ne_descend_jamais_sous_zero(self):
        """Meme avec beaucoup d'erreurs, le score ne doit jamais etre negatif."""
        self.assertEqual(scores.calculer_score("chat", 10, "facile"), 0)

    def test_difficile_rapporte_plus_que_facile(self):
        """A erreurs egales, un mot en difficile doit rapporter plus qu'en facile."""
        score_facile = scores.calculer_score("hibou", 0, "facile")
        score_difficile = scores.calculer_score("hibou", 0, "difficile")
        self.assertGreater(score_difficile, score_facile)


class TestSauvegardeScores(unittest.TestCase):

    def setUp(self):
        """Redirige la sauvegarde vers un fichier temporaire pour ne pas toucher aux vrais scores."""
        self.fichier_original = scores.FICHIER_SCORES
        scores.FICHIER_SCORES = "test_scores_temp.json"

    def tearDown(self):
        """Supprime le fichier temporaire et restaure le vrai chemin des scores."""
        if os.path.exists(scores.FICHIER_SCORES):
            os.remove(scores.FICHIER_SCORES)
        scores.FICHIER_SCORES = self.fichier_original

    def test_sauvegarder_puis_charger(self):
        scores.sauvegarder_score("TestJoueur", 100, "moyen", "python")
        resultats = scores.charger_scores()
        self.assertEqual(len(resultats), 1)
        self.assertEqual(resultats[0]["nom"], "TestJoueur")
        self.assertEqual(resultats[0]["score"], 100)

    def test_charger_fichier_inexistant_retourne_liste_vide(self):
        resultats = scores.charger_scores()
        self.assertEqual(resultats, [])


if __name__ == "__main__":
    unittest.main()