import requests
import json
import os
from dotenv import load_dotenv, set_key

# Charger les variables d'environnement
load_dotenv()
USERNAME = os.getenv("LW_USERNAME")
PASSWORD = os.getenv("LW_PASSWORD")
PLAYER_ID = os.getenv("PLAYER_ID")
ENV_FILE = ".env"

API_URL = "https://leekwars.com/api/"
AIS_FILE = "scripts_ia/my_ais.json"
OUTPUT_DIR = "scripts_ia"

session = requests.Session()  # 🔥 Utilisation d'une session persistante

# Créer le dossier des scripts IA s'il n'existe pas
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_auth_token():
    """Récupère un token d'authentification via /farmer/login-token et l'enregistre"""
    global session

    url = f"{API_URL}farmer/login-token"
    data = {
        "login": USERNAME,
        "password": PASSWORD
    }

    response = session.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        if "token" in result:
            token = result["token"].strip()
            print(f"✅ Token obtenu : {token[:10]}... (tronqué)")

            # 🔥 Sauvegarde du token sans guillemets
            with open(ENV_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(ENV_FILE, "w", encoding="utf-8") as f:
                for line in lines:
                    if not line.startswith("LW_TOKEN="):
                        f.write(line)
                f.write(f'LW_TOKEN={token}\n')

            print(f"📁 Token sauvegardé dans {ENV_FILE} sans guillemets.")
            return token
        else:
            print("❌ Erreur : Aucun token retourné.")
            return None
    else:
        print(f"❌ Erreur API (get_auth_token) : {response.json()}")
        return None


def get_valid_token():
    """Vérifie si le token est valide, sinon en génère un nouveau"""
    global session
    TOKEN = os.getenv("LW_TOKEN")

    url = f"{API_URL}ai/get-farmer-ais"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = session.get(url, headers=headers)  # 🔥 Envoi du token dans les headers

    if response.status_code == 401:
        print("❌ Token invalide ou expiré. Obtention d'un nouveau token...")
        TOKEN = get_auth_token()

    return TOKEN


def get_farmer_ais():
    """Récupère toutes les IA du joueur et les sauvegarde."""
    token = get_valid_token()
    url = f"{API_URL}ai/get-farmer-ais"
    headers = {"Authorization": f"Bearer {token}"}

    response = session.get(url, headers=headers)  # 🔥 Utilisation des headers

    if response.status_code == 200:
        data = response.json()
        if "ais" in data:
            ais = data["ais"]

            # Sauvegarde en JSON
            with open(AIS_FILE, "w", encoding="utf-8") as f:
                json.dump(ais, f, indent=4)

            print(f"✅ {len(ais)} IA récupérées et sauvegardées dans `{AIS_FILE}`")
            return ais
        else:
            print("❌ Aucune IA trouvée.")
            return None
    else:
        print(f"❌ Erreur API : {response.status_code}")
        print(response.json())
        return None

def get_ai_code(ai_id, ai_name):
    """Récupère le code source d'une IA spécifique et le sauvegarde"""
    token = get_valid_token()
    url = f"{API_URL}ai/get/{ai_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = session.get(url, headers=headers)  # 🔥 Envoi du token en header

    if response.status_code == 200:
        data = response.json()
        if "ai" in data and "code" in data["ai"]:
            code = data["ai"]["code"]

            # Sauvegarde du code dans un fichier .leek
            filename = f"{OUTPUT_DIR}/{ai_name.replace(' ', '_')}.leek"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"✅ Code de `{ai_name}` sauvegardé dans `{filename}`")
            return True
        else:
            print(f"❌ Aucune donnée de code pour `{ai_name}`")
            return False
    else:
        print(f"❌ Erreur API pour `{ai_name}` : {response.status_code}")
        print(response.json())
        return False

def get_all_ai_codes():
    """Récupère et sauvegarde le code de toutes les IA du joueur"""
    if not os.path.exists(AIS_FILE):
        print(f"❌ Fichier `{AIS_FILE}` introuvable. Exécute `get_farmer_ais()` d'abord.")
        return

    with open(AIS_FILE, "r", encoding="utf-8") as f:
        ais = json.load(f)

    print(f"📡 Récupération du code pour {len(ais)} IA...")

    for ai in ais:
        get_ai_code(ai["id"], ai["name"])
