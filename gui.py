"""Interface graphique du jeu du Pendu, avec tkinter."""

import string
import tkinter as tk
from tkinter import ttk, messagebox

from mots import CATEGORIES, DIFFICULTES, choisir_mot
from scores import calculer_score, sauvegarder_score, obtenir_meilleurs_scores
from dessins import DESSINS_PENDU

ERREURS_MAX = 6


class PenduGUI:
    """Fenetre principale du jeu du Pendu en version graphique."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Le Pendu")
        self.root.geometry("520x680")
        self.root.resizable(False, False)

        self.mot: str = ""
        self.lettres_trouvees: set[str] = set()
        self.lettres_essayees: set[str] = set()
        self.erreurs: int = 0
        self.difficulte: str = "facile"
        self.boutons_lettres: dict[str, tk.Button] = {}

        self._construire_interface()

    def _construire_interface(self) -> None:
        """Construit tous les widgets de la fenetre."""
        cadre_haut = tk.Frame(self.root)
        cadre_haut.pack(pady=10)

        tk.Label(cadre_haut, text="Nom :").grid(row=0, column=0, padx=5, sticky="e")
        self.entree_nom = tk.Entry(cadre_haut, width=15)
        self.entree_nom.insert(0, "Joueur")
        self.entree_nom.grid(row=0, column=1, padx=5)

        tk.Label(cadre_haut, text="Categorie :").grid(row=0, column=2, padx=5, sticky="e")
        self.categorie_var = tk.StringVar(value=list(CATEGORIES.keys())[0])
        ttk.Combobox(
            cadre_haut, textvariable=self.categorie_var,
            values=list(CATEGORIES.keys()), width=13, state="readonly",
        ).grid(row=0, column=3, padx=5)

        tk.Label(cadre_haut, text="Difficulte :").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.difficulte_var = tk.StringVar(value=list(DIFFICULTES.keys())[0])
        ttk.Combobox(
            cadre_haut, textvariable=self.difficulte_var,
            values=list(DIFFICULTES.keys()), width=13, state="readonly",
        ).grid(row=1, column=1, padx=5, pady=8)

        tk.Button(
            cadre_haut, text="Nouvelle partie", command=self.nouvelle_partie, bg="#4CAF50", fg="white"
        ).grid(row=1, column=2, columnspan=2, padx=5, pady=8, sticky="we")

        self.label_dessin = tk.Label(self.root, text=DESSINS_PENDU[0], font=("Courier", 12), justify="left")
        self.label_dessin.pack(pady=5)

        self.label_mot = tk.Label(self.root, text="", font=("Courier", 22, "bold"))
        self.label_mot.pack(pady=10)

        self.label_statut = tk.Label(
            self.root, text="Clique sur 'Nouvelle partie' pour commencer.", font=("Arial", 11)
        )
        self.label_statut.pack(pady=5)

        cadre_lettres = tk.Frame(self.root)
        cadre_lettres.pack(pady=10)
        for i, lettre in enumerate(string.ascii_lowercase):
            bouton = tk.Button(
                cadre_lettres, text=lettre.upper(), width=3,
                command=lambda l=lettre: self.proposer_lettre(l),
            )
            bouton.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            self.boutons_lettres[lettre] = bouton

        # Couleur par defaut reelle du systeme (portable Windows/Linux/Mac)
        self.couleur_defaut = next(iter(self.boutons_lettres.values())).cget("bg")

        self.label_scores = tk.Label(self.root, text="", font=("Arial", 10), justify="left")
        self.label_scores.pack(pady=15)

        self.desactiver_lettres()
        self.mettre_a_jour_scores()

    def desactiver_lettres(self) -> None:
        """Desactive tous les boutons de lettres (avant le debut d'une partie)."""
        for bouton in self.boutons_lettres.values():
            bouton.config(state="disabled")

    def activer_lettres(self) -> None:
        """Reactive tous les boutons de lettres avec leur couleur par defaut."""
        for bouton in self.boutons_lettres.values():
            bouton.config(state="normal", bg=self.couleur_defaut)

    def mettre_a_jour_scores(self) -> None:
        """Rafraichit l'affichage du classement des meilleurs scores."""
        scores = obtenir_meilleurs_scores(5)
        if not scores:
            texte = "Aucun score enregistre pour le moment."
        else:
            lignes = [f"{i + 1}. {s['nom']} - {s['score']} pts ({s['difficulte']})" for i, s in enumerate(scores)]
            texte = "Meilleurs scores :\n" + "\n".join(lignes)
        self.label_scores.config(text=texte)

    def nouvelle_partie(self) -> None:
        """Demarre une nouvelle partie avec la categorie et la difficulte choisies."""
        categorie = self.categorie_var.get()
        self.difficulte = self.difficulte_var.get()
        self.mot = choisir_mot(categorie, self.difficulte)
        self.lettres_trouvees = set()
        self.lettres_essayees = set()
        self.erreurs = 0

        self.activer_lettres()
        self.label_dessin.config(text=DESSINS_PENDU[0])
        self.label_statut.config(text=f"Categorie : {categorie} | Difficulte : {self.difficulte}", fg="black")
        self._rafraichir_mot()

    def _rafraichir_mot(self) -> None:
        """Met a jour l'affichage du mot avec les lettres trouvees et les tirets."""
        affichage = " ".join(l if l in self.lettres_trouvees else "_" for l in self.mot)
        self.label_mot.config(text=affichage)

    def proposer_lettre(self, lettre: str) -> None:
        """Traite le clic sur un bouton de lettre.

        Args:
            lettre: La lettre proposee par le joueur.
        """
        if not self.mot:
            messagebox.showinfo("Info", "Clique d'abord sur 'Nouvelle partie'.")
            return

        self.lettres_essayees.add(lettre)
        self.boutons_lettres[lettre].config(state="disabled")

        if lettre in self.mot:
            self.lettres_trouvees.add(lettre)
            self.boutons_lettres[lettre].config(bg="lightgreen")
            self.label_statut.config(text="Bonne lettre !", fg="green")
        else:
            self.erreurs += 1
            self.boutons_lettres[lettre].config(bg="lightcoral")
            self.label_statut.config(text="Mauvaise lettre !", fg="red")

        self.label_dessin.config(text=DESSINS_PENDU[self.erreurs])
        self._rafraichir_mot()

        if all(l in self.lettres_trouvees for l in self.mot):
            self._fin_partie(gagne=True)
        elif self.erreurs >= ERREURS_MAX:
            self._fin_partie(gagne=False)

    def _fin_partie(self, gagne: bool) -> None:
        """Termine la partie, sauvegarde le score et affiche le resultat.

        Args:
            gagne: True si le joueur a trouve le mot, False sinon.
        """
        nom_joueur = self.entree_nom.get().strip() or "Joueur"
        self.desactiver_lettres()

        if gagne:
            score = calculer_score(self.mot, self.erreurs, self.difficulte)
            sauvegarder_score(nom_joueur, score, self.difficulte, self.mot)
            self.label_statut.config(text=f"BRAVO ! Score : {score} points", fg="green")
            messagebox.showinfo("Gagne !", f"Bravo, tu as trouve '{self.mot}' !\nScore : {score} points")
        else:
            sauvegarder_score(nom_joueur, 0, self.difficulte, self.mot)
            self.label_statut.config(text=f"PERDU ! Le mot etait : {self.mot}", fg="red")
            messagebox.showinfo("Perdu", f"Dommage ! Le mot etait : {self.mot}")

        self.mettre_a_jour_scores()


def main() -> None:
    """Lance la fenetre principale du jeu."""
    root = tk.Tk()
    PenduGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()