import os
import requests
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("LW_TOKEN")
PLAYER_ID = os.getenv("PLAYER_ID")

API_URL = "https://leekwars.com/api/"
UPLOAD_DIR = "scripts_to_upload"
EXTENSION_TARGET = ".leek"
UPLOADED_SCRIPTS_FILE = "uploaded_scripts.json"
DEFAULT_FOLDER_ID = 0  # Dossier racine par défaut
DEFAULT_VERSION = 1  # Version par défaut pour les IA

os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_existing_ais():
    """Récupère la liste des IA du joueur et leurs IDs"""
    url = f"{API_URL}ai/get-farmer-ais"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "ais" in data:
            return {ai["name"]: ai["id"] for ai in data["ais"]}
    else:
        print(f"❌ Erreur API lors de la récupération des IA : {response.json()}")

    return {}


def create_ai(ai_name):
    """Crée une nouvelle IA sur Leek Wars et retourne son ID"""
    url = f"{API_URL}ai/new-name"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "folder_id": DEFAULT_FOLDER_ID,
        "version": DEFAULT_VERSION,
        "name": ai_name
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        if "ai" in result and "id" in result["ai"]:
            print(f"✅ IA `{ai_name}` créée avec ID {result['ai']['id']}")
            return result["ai"]["id"]
    else:
        print(f"❌ Erreur lors de la création de `{ai_name}` : {response.json()}")

    return None


def upload_ai_script(file_path, ai_id):
    """Upload un script .leek sur Leek Wars"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    url = f"{API_URL}ai/save"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"ai_id": ai_id, "code": code}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f"✅ IA `{os.path.basename(file_path)}` mise à jour avec succès !")
        return {"name": os.path.basename(file_path), "status": "uploaded"}
    else:
        print(f"❌ Erreur lors de l'upload de `{os.path.basename(file_path)}` : {response.status_code}")
        print(response.json())
        return {"name": os.path.basename(file_path), "status": "error"}


def upload_all_scripts():
    """Upload tous les fichiers .leek du dossier `scripts_to_upload/` sur Leek Wars"""
    existing_ais = get_existing_ais()

    scripts = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(EXTENSION_TARGET)]
    if not scripts:
        print("❌ Aucun script .leek trouvé dans `scripts_to_upload/`.")
        return

    print(f"📡 Upload de {len(scripts)} scripts IA vers Leek Wars...")

    results = []
    for script in scripts:
        file_path = os.path.join(UPLOAD_DIR, script)
        ai_name = os.path.splitext(script)[0]

        # Vérifier si l'IA existe déjà
        ai_id = existing_ais.get(ai_name)

        if not ai_id:
            print(f"🔄 IA `{ai_name}` non trouvée. Création en cours...")
            ai_id = create_ai(ai_name)

        if ai_id:
            result = upload_ai_script(file_path, ai_id)
            results.append(result)
        else:
            print(f"❌ Impossible d'upload `{ai_name}` (échec de récupération/création).")

    # Sauvegarde des résultats dans un fichier
    with open(UPLOADED_SCRIPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"📁 Résultats sauvegardés dans `{UPLOADED_SCRIPTS_FILE}`.")


if __name__ == "__main__":
    if not TOKEN or not PLAYER_ID:
        print("❌ Token ou Player ID manquant. Exécute `get_token.py` pour en obtenir un.")
    else:
        upload_all_scripts()
