#!/bin/bash
# Lance l'interface graphique du Pendu, peu importe le dossier depuis lequel on l'appelle.

DOSSIER_SCRIPT="$(dirname "$(readlink -f "$0")")"
cd "$DOSSIER_SCRIPT" || exit 1
python3 gui.py