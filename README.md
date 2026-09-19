# jeu_pendu_python
## 1er projet en python; qui va constituer a créer un jeu à partir de mon debian linux et des outils de python3


# Jeu du Pendu (Python)

Un jeu du Pendu complet en Python, jouable dans le terminal, avec catégories de mots, niveaux de difficulté, système de score et sauvegarde des meilleurs scores.

Projet réalisé par Mel dans le cadre de l'apprentissage de Python et de la ligne de commande Linux (Debian via WSL2).

## Fonctionnalités

- 3 catégories de mots : informatique, cybersécurité, animaux
- 3 niveaux de difficulté (facile, moyen, difficile) selon la longueur des mots
- Dessin ASCII du pendu qui évolue à chaque erreur
- Système de score (bonus selon la difficulté, pénalité par erreur)
- Sauvegarde des meilleurs scores dans un fichier local (`scores.json`)
- Option pour rejouer plusieurs parties sans relancer le programme
- Gestion propre de l'interruption (Ctrl+C)
- Tests automatisés (module `unittest`)

## Structure du projet

```
pendu_en_python/
├── jeu.py           # Point d'entree, boucle de jeu principale
├── mots.py          # Categories de mots, choix de la difficulte
├── scores.py        # Calcul et sauvegarde des scores
├── dessins.py        # Dessins ASCII du pendu
├── test_jeu.py       # Tests pour l'affichage du mot
├── test_mots.py       # Tests pour la selection des mots
├── test_scores.py     # Tests pour le calcul et la sauvegarde des scores
└── README.md
```

## Prérequis

- Python 3.10 ou plus récent (utilise les type hints modernes comme `list[str]`)
- Aucune dépendance externe : uniquement des modules déjà inclus avec Python (`random`, `json`, `os`)

## Installation et lancement

```bash
git clone https://github.com/melchisedek21/jeu_pendu_python.git
cd jeu_pendu_python
python3 jeu.py
```

## Comment jouer

1. Entre ton nom au démarrage
2. Choisis une catégorie de mots
3. Choisis un niveau de difficulté
4. Propose une lettre à la fois
5. Devine le mot avant d'atteindre 6 erreurs !

Ton score est calculé selon la longueur du mot, le nombre d'erreurs et la difficulté choisie, puis sauvegardé automatiquement.

## Lancer les tests

```bash
python3 -m unittest discover -v
```

## Améliorations possibles

- Interface graphique avec `tkinter`
- Mode multijoueur (un joueur propose le mot à un autre)
- Minuteur par lettre
- Plus de catégories de mots