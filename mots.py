"""Gestion des categories de mots et de la selection selon la difficulte."""

import random

CATEGORIES: dict[str, list[str]] = {
    "informatique": [
        "python", "ordinateur", "clavier", "debian", "programme", "reseau", "logiciel",
        "souris", "ecran", "processeur", "memoire", "disque", "serveur", "fichier",
        "dossier", "systeme", "application", "navigateur", "connexion", "wifi",
        "bluetooth", "imprimante", "carte", "ventilateur", "boitier", "moniteur",
        "cable", "routeur", "modem", "terminal", "commande", "fonction", "variable",
        "boucle", "tableau", "algorithme", "compilateur", "code", "script", "base",
        "donnees", "internet", "site", "page", "materiel", "linux",
        "windows", "mobile", "tablette",
    ],
    "cybersecurite": [
        "hacker", "virus", "pentest", "firewall", "malware", "chiffrement", "phishing",
        "vulnerabilite", "cryptographie", "motdepasse", "antivirus", "spam", "backdoor",
        "exploit", "ransomware", "trojan", "audit", "intrusion", "authentification",
        "biometrie", "jeton", "certificat", "proxy", "sandbox", "keylogger", "spoofing",
        "injection", "cookie", "attaque", "defense", "risque", "menace", "protocole",
        "chiffre", "cle", "signature", "sauvegarde", "acces", "utilisateur", "session",
        "vpn", "port", "scan", "faille", "correctif",
    ],
    "animaux": [
        "elephant", "girafe", "kangourou", "tortue", "dauphin", "hibou", "rhinoceros",
        "lion", "tigre", "zebre", "singe", "panda", "koala", "loup", "renard", "ours",
        "aigle", "faucon", "serpent", "crocodile", "iguane", "cameleon", "papillon",
        "abeille", "fourmi", "araignee", "requin", "baleine", "phoque", "pingouin",
        "autruche", "flamant", "perroquet", "hamster", "ecureuil", "herisson", "chat",
        "chien", "cheval", "vache", "cochon", "mouton", "chevre", "lapin", "souris",
        "canard", "poule", "dindon", "chameau", "buffle",
    ],
}

DIFFICULTES: dict[str, tuple[int, int]] = {
    "facile": (4, 6),
    "moyen": (7, 9),
    "difficile": (10, 99),
}


def choisir_categorie() -> str:
    """Demande au joueur de choisir une categorie parmi celles disponibles.

    Returns:
        Le nom de la categorie choisie.
    """
    print("Categories disponibles :")
    for nom in CATEGORIES:
        print(f" - {nom}")
    while True:
        choix = input("Choisis une categorie : ").lower().strip()
        if choix in CATEGORIES:
            return choix
        print("Categorie inconnue, reessaie.")


def choisir_difficulte() -> str:
    """Demande au joueur de choisir une difficulte.

    Returns:
        Le nom de la difficulte choisie (facile, moyen ou difficile).
    """
    print("\nDifficultes disponibles : facile, moyen, difficile")
    while True:
        choix = input("Choisis une difficulte : ").lower().strip()
        if choix in DIFFICULTES:
            return choix
        print("Difficulte inconnue, reessaie.")


def choisir_mot(categorie: str, difficulte: str) -> str:
    """Choisit un mot au hasard dans une categorie, filtre par longueur selon la difficulte.

    Args:
        categorie: Le nom de la categorie (doit exister dans CATEGORIES).
        difficulte: Le nom de la difficulte (doit exister dans DIFFICULTES).

    Returns:
        Un mot au hasard respectant la plage de longueur de la difficulte.
    """
    min_len, max_len = DIFFICULTES[difficulte]
    mots_possibles = [m for m in CATEGORIES[categorie] if min_len <= len(m) <= max_len]
    if not mots_possibles:
        mots_possibles = CATEGORIES[categorie]
    return random.choice(mots_possibles)