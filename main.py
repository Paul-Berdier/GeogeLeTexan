from leekwars_bot.api import get_farmer_ais, get_all_ai_codes

if __name__ == "__main__":
    print("📡 Vérification et récupération du token...")
    get_farmer_ais()

    print("\n📡 Récupération des scripts IA...")
    get_all_ai_codes()
