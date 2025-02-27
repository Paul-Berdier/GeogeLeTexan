import json
import os

DATA_DIR = "data"

# Créer le dossier de stockage s'il n'existe pas
os.makedirs(DATA_DIR, exist_ok=True)

def save_json(filename, data):
    """Sauvegarde les données en JSON"""
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Données sauvegardées dans {path}")

def load_json(filename):
    """Charge les données depuis un fichier JSON"""
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
