import os
import re

# Dossier contenant tes icônes téléchargées
ICON_DIR = "frontend/capacites"
PORTRAIT_DIR = "frontend/portraits"

# Regex pour enlever le hash (8 caractères hexadécimaux) avant .png
HASH_RE = re.compile(r'_[0-9a-f]{8}(?=\.png)')

for filename in os.listdir(ICON_DIR):
    if filename.endswith(".png"):
        new_name = HASH_RE.sub('', filename)
        if new_name != filename:
            old_path = os.path.join(ICON_DIR, filename)
            new_path = os.path.join(ICON_DIR, new_name)
            os.rename(old_path, new_path)
            print(f"Renommé : {filename} -> {new_name}")

for filename in os.listdir(PORTRAIT_DIR):
    if filename.endswith(".png"):
        new_name = HASH_RE.sub('', filename)
        if new_name != filename:
            old_path = os.path.join(PORTRAIT_DIR, filename)
            new_path = os.path.join(PORTRAIT_DIR, new_name)
            os.rename(old_path, new_path)
            print(f"Renommé : {filename} -> {new_name}")

print("Tous les fichiers ont été renommés !")
