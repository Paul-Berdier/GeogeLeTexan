import os

SCRIPTS_DIR = "scripts_to_upload"
OUTPUT_FILE = "scripts_ia/combined.leek"

def merge_scripts():
    """Fusionne tous les fichiers .leek en un seul"""
    if not os.path.exists(SCRIPTS_DIR):
        print(f"❌ Dossier `{SCRIPTS_DIR}` introuvable.")
        return

    scripts = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".leek")]
    if not scripts:
        print("❌ Aucun script .leek trouvé à fusionner.")
        return

    print(f"📡 Fusion de {len(scripts)} scripts en `{OUTPUT_FILE}`...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write("// Script fusionné généré automatiquement\n\n")
        for script in scripts:
            file_path = os.path.join(SCRIPTS_DIR, script)
            with open(file_path, "r", encoding="utf-8") as f:
                output.write(f"\n// --- Début de `{script}` ---\n")
                output.write(f.read())
                output.write(f"\n// --- Fin de `{script}` ---\n\n")

    print(f"✅ Fusion terminée. Résultat dans `{OUTPUT_FILE}`.")

if __name__ == "__main__":
    merge_scripts()
