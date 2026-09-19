"""Point d'entree du jeu du Pendu."""

import os

from mots import choisir_categorie, choisir_difficulte, choisir_mot
from scores import calculer_score, sauvegarder_score, afficher_meilleurs_scores
from dessins import DESSINS_PENDU

ERREURS_MAX = 6

# Empeche le terminal d'afficher "^C" quand on appuie sur Ctrl+C (Linux/Mac uniquement)
os.system("stty -echoctl 2>/dev/null")


def afficher_mot(mot: str, lettres_trouvees: set[str]) -> str:
    """Construit l'affichage du mot avec des tirets pour les lettres non trouvees.

    Args:
        mot: Le mot secret.
        lettres_trouvees: L'ensemble des lettres deja devinees correctement.

    Returns:
        Une chaine du type "p _ t _ o n" prete a etre affichee.
    """
    affichage = ""
    for lettre in mot:
        affichage += (lettre + " ") if lettre in lettres_trouvees else "_ "
    return affichage.strip()


def jouer_une_partie(nom_joueur: str) -> None:
    """Joue une partie complete du Pendu, du choix de categorie jusqu'a la fin.

    Args:
        nom_joueur: Le nom du joueur, utilise pour sauvegarder le score.
    """
    categorie = choisir_categorie()
    difficulte = choisir_difficulte()
    mot = choisir_mot(categorie, difficulte)

    lettres_trouvees: set[str] = set()
    lettres_essayees: set[str] = set()
    erreurs = 0

    print(f"\nCategorie : {categorie} | Difficulte : {difficulte}")
    print(f"Le mot a deviner contient {len(mot)} lettres.")

    while erreurs < ERREURS_MAX:
        print(DESSINS_PENDU[erreurs])
        print(afficher_mot(mot, lettres_trouvees))
        print(f"Erreurs : {erreurs}/{ERREURS_MAX}")
        print(f"Lettres deja essayees : {', '.join(sorted(lettres_essayees)) if lettres_essayees else 'aucune'}")

        if all(lettre in lettres_trouvees for lettre in mot):
            score = calculer_score(mot, erreurs, difficulte)
            print(f"\nBRAVO ! Tu as trouve le mot : {mot}")
            print(f"Score obtenu : {score} points")
            sauvegarder_score(nom_joueur, score, difficulte, mot)
            return

        proposition = input("Propose une lettre : ").lower().strip()

        if len(proposition) != 1 or not proposition.isalpha() or not proposition.isascii():
            print("Merci de proposer une seule lettre valide (a-z, sans accent).")
            continue

        if proposition in lettres_essayees:
            print("Tu as deja essaye cette lettre.")
            continue

        lettres_essayees.add(proposition)

        if proposition in mot:
            lettres_trouvees.add(proposition)
            print("Bonne lettre !")
        else:
            erreurs += 1
            print("Mauvaise lettre !")

    print(DESSINS_PENDU[erreurs])
    print(f"\nPERDU ! Le mot etait : {mot}")
    sauvegarder_score(nom_joueur, 0, difficulte, mot)


def main() -> None:
    """Boucle principale : gere le nom du joueur et les parties successives."""
    print("=== BIENVENUE DANS LE PENDU ===")
    nom_joueur = input("Quel est ton nom ? ").strip() or "Joueur"

    while True:
        afficher_meilleurs_scores()
        jouer_une_partie(nom_joueur)

        rejouer = input("\nVeux-tu rejouer ? (oui/non) : ").lower().strip()
        if rejouer != "oui":
            print("Merci d'avoir joue, a bientot !")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPartie interrompue. A bientot !")