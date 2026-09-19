"""Gestion du calcul de score et de la sauvegarde/lecture des meilleurs scores."""

import json
import os

FICHIER_SCORES = "scores.json"

MULTIPLICATEUR_SCORE: dict[str, float] = {
    "facile": 1,
    "moyen": 1.5,
    "difficile": 2,
}


def calculer_score(mot: str, erreurs: int, difficulte: str) -> int:
    """Calcule le score obtenu pour un mot devine.

    Args:
        mot: Le mot devine.
        erreurs: Le nombre d'erreurs commises pendant la partie.
        difficulte: La difficulte de la partie (influence le multiplicateur).

    Returns:
        Le score final, jamais negatif.
    """
    base = len(mot) * 10
    penalite = erreurs * 5
    score = (base - penalite) * MULTIPLICATEUR_SCORE[difficulte]
    return max(0, round(score))


def charger_scores() -> list[dict]:
    """Charge la liste des scores depuis le fichier JSON.

    Returns:
        Une liste de dictionnaires de scores. Liste vide si le fichier n'existe pas
        ou est corrompu.
    """
    if not os.path.exists(FICHIER_SCORES):
        return []
    try:
        with open(FICHIER_SCORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def sauvegarder_score(nom_joueur: str, score: int, difficulte: str, mot: str) -> None:
    """Ajoute un nouveau score a la liste existante et sauvegarde dans le fichier JSON.

    Args:
        nom_joueur: Le nom du joueur.
        score: Le score obtenu.
        difficulte: La difficulte de la partie.
        mot: Le mot qui etait a deviner.
    """
    scores = charger_scores()
    scores.append({
        "nom": nom_joueur,
        "score": score,
        "difficulte": difficulte,
        "mot": mot,
    })
    try:
        with open(FICHIER_SCORES, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
    except OSError:
        print("Attention : impossible de sauvegarder le score (probleme de fichier).")


def obtenir_meilleurs_scores(top_n: int = 5) -> list[dict]:
    """Retourne les meilleurs scores enregistres, tries du plus haut au plus bas.

    Args:
        top_n: Le nombre de scores a retourner (5 par defaut).

    Returns:
        Une liste de dictionnaires de scores, triee par score decroissant.
    """
    scores = charger_scores()
    return sorted(scores, key=lambda s: s["score"], reverse=True)[:top_n]


def afficher_meilleurs_scores(top_n: int = 5) -> None:
    """Affiche le classement des meilleurs scores enregistres (version terminal).

    Args:
        top_n: Le nombre de scores a afficher (5 par defaut).
    """
    scores_tries = obtenir_meilleurs_scores(top_n)
    if not scores_tries:
        print("Aucun score enregistre pour le moment.")
        return
    print(f"\n=== TOP {top_n} MEILLEURS SCORES ===")
    for i, s in enumerate(scores_tries, start=1):
        print(f"{i}. {s['nom']} - {s['score']} pts ({s['difficulte']}, mot: {s['mot']})")