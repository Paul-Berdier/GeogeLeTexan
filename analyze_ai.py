import os
import re
import json

SCRIPTS_DIR = "scripts_ia"
ANALYSIS_FILE = "ai_analysis.json"

# Expressions régulières pour identifier les actions dans le code
ACTION_PATTERNS = {
    "move": r"\bmoveToward\(",
    "attack": r"\battack\(",
    "heal": r"\bheal\(",
    "buff": r"\bbuff\(",
    "debuff": r"\bdebuff\(",
    "use_chip": r"\buseChip\(",
    "if_conditions": r"\bif\s*\(.*\)",
    "loops": r"\b(for|while)\s*\(.*\)",
}

def analyze_script(file_path):
    """Analyse un script .leek et extrait des informations clés"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    analysis = {"name": os.path.basename(file_path), "actions": {}}

    # Compter les occurrences de chaque type d'action
    for action, pattern in ACTION_PATTERNS.items():
        matches = re.findall(pattern, code)
        analysis["actions"][action] = len(matches)

    return analysis

def analyze_all_scripts():
    """Analyse tous les scripts d'IA présents dans `scripts_ia/`"""
    if not os.path.exists(SCRIPTS_DIR):
        print(f"❌ Dossier `{SCRIPTS_DIR}` introuvable. Lance `main.py` pour récupérer les scripts.")
        return

    scripts = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".leek")]
    if not scripts:
        print("❌ Aucun script trouvé dans `scripts_ia/`.")
        return

    print(f"📡 Analyse de {len(scripts)} scripts IA...")

    results = []
    for script in scripts:
        file_path = os.path.join(SCRIPTS_DIR, script)
        results.append(analyze_script(file_path))

    # Sauvegarde des résultats
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"✅ Analyse terminée. Résultats sauvegardés dans `{ANALYSIS_FILE}`.")

if __name__ == "__main__":
    analyze_all_scripts()
